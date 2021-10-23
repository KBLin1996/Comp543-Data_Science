import java.io.IOException;
import java.util.*;

import org.apache.hadoop.util.ToolRunner;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import org.apache.hadoop.util.Tool;
import org.apache.hadoop.conf.Configured;


public class WordCount extends Configured implements Tool {

    static int printUsage() {
        System.out.println("wordcount [-m <maps>] [-r <reduces>] <input> <output>");
        ToolRunner.printGenericCommandUsage(System.out);
        return -1;
    }

    public static class Pair {
        String key;
        Double value;

        public Pair (String s, Double d) {
            this.key = s;
            this.value = d;
        }
    }

    static class Compare implements Comparator<Pair> {
        @Override
        public int compare(Pair p1, Pair p2) {
            if (p1.value > p2.value) {
                return 1;
            } else if (p1.value < p2.value) {
                return -1;
            }
            return 0;
        }
    }

    public static class WordCountMapper extends Mapper<Object, Text, Text, Text> {
        PriorityQueue<Pair> pq = new PriorityQueue<>(new Compare());

        // Key and value for context.write()
        private Text generalID = new Text();
        private Text revenueID = new Text();

        public void cleanup(Context context) throws IOException, InterruptedException {
            while (pq.size() != 0) {
                String unionKey = "key";
                Pair p = pq.poll();
                generalID.set(unionKey);
                revenueID.set(p.key + "," + p.value.toString());
                context.write(generalID, revenueID);
            }
        }

        public void map(Object key, Text value, Context context) throws IOException, InterruptedException {
            StringTokenizer itr = new StringTokenizer(value.toString(), "\t");
            String id = "";
            boolean isString = true;

            while (itr.hasMoreTokens()) {
                String nextToken = itr.nextToken();

                if (isString) {
                    id = nextToken;
                    isString = false;
                } else {
                    Double amount = Double.parseDouble(nextToken);

                    if (pq.size() < 5) {
                        pq.add(new Pair(id, amount));
                    } else {
                        if (amount > pq.peek().value) {
                            pq.poll();
                            pq.add(new Pair(id, amount));
                        }
                    }
                    isString = true;
                }
            }
        }
    }

    public static class WordCountReducer extends Reducer<Text, Text, Text, Text> {
        // Key and value for context.write()
        private Text finalID = new Text();
        private Text revenue = new Text();

        public void reduce(Text key, Iterable<Text> values, Context context) throws IOException, InterruptedException {
            PriorityQueue<Pair> pqReduce = new PriorityQueue<>(new Compare());

            for (Text val : values) {
                String s = val.toString();
                String taxiID = s.split(",")[0];
                Double amount = Double.parseDouble(s.split(",")[1]);

                if (pqReduce.size() < 5) {
                    pqReduce.add(new Pair(taxiID, amount));
                } else {
                    if (amount > pqReduce.peek().value) {
                        pqReduce.poll();
                        pqReduce.add(new Pair(taxiID, amount));
                    }
                }
            }

            for (Pair pr : pqReduce) {
                finalID.set(pr.key);
                revenue.set(pr.value.toString());
                context.write(finalID, revenue);
            }
        }
    }

    public int run(String[] args) throws Exception {

        Configuration conf = new Configuration();
        Job job = Job.getInstance(conf, "word count");
        job.setJarByClass(WordCount.class);
        job.setMapperClass(WordCountMapper.class);
        job.setReducerClass(WordCountReducer.class);
        job.setOutputKeyClass(Text.class);
        job.setOutputValueClass(Text.class);

        List<String> other_args = new ArrayList<String>();
        for(int i=0; i < args.length; ++i) {
            try {
                if ("-r".equals(args[i])) {
                    job.setNumReduceTasks(Integer.parseInt(args[++i]));
                } else {
                    other_args.add(args[i]);
                }
            } catch (NumberFormatException except) {
                System.out.println("ERROR: Integer expected instead of " + args[i]);
                return printUsage();
            } catch (ArrayIndexOutOfBoundsException except) {
                System.out.println("ERROR: Required parameter missing from " +
                        args[i-1]);
                return printUsage();
            }
        }
        // Make sure there are exactly 2 parameters left.
        if (other_args.size() != 2) {
            System.out.println("ERROR: Wrong number of parameters: " +
                    other_args.size() + " instead of 2.");
            return printUsage();
        }
        FileInputFormat.setInputPaths(job, other_args.get(0));
        FileOutputFormat.setOutputPath(job, new Path(other_args.get(1)));
        return (job.waitForCompletion(true) ? 0 : 1);
    }

    public static void main(String[] args) throws Exception {
        int res = ToolRunner.run(new Configuration(), new WordCount(), args);
        System.exit(res);
    }
}
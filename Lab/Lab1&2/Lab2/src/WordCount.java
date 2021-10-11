import java.io.IOException;
import java.util.StringTokenizer;

import org.apache.hadoop.util.ToolRunner;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import org.apache.hadoop.util.Tool;
import org.apache.hadoop.conf.Configured;
import java.util.ArrayList;
import java.util.List;
import java.util.regex.Pattern;
import java.util.regex.Matcher;

public class WordCount extends Configured implements Tool {

    static int printUsage() {
        System.out.println("wordcount [-m <maps>] [-r <reduces>] <input> <output>");
        ToolRunner.printGenericCommandUsage(System.out);
        return -1;
    }

    public static class WordCountMapper
            extends Mapper<Object, Text, Text, IntWritable> {

        // so we don't have to do reallocations
        private final static IntWritable one = new IntWritable(1);
        private Text word = new Text();

        // to check for only alphanumeric
        String expression = "^[a-zA-Z]*$";
        String prevToken = "";
        String outputString = "";
        Pattern pattern = Pattern.compile(expression);

        public void map(Object key, Text value, Context context) throws IOException, InterruptedException {
            StringTokenizer itr = new StringTokenizer(value.toString());
            while (itr.hasMoreTokens()) {
                // check for all alphabetical
                String nextToken = itr.nextToken();
                if (prevToken.equals("")) {
                    prevToken = itr.nextToken();
                    outputString = nextToken + ", " + prevToken;
                    nextToken = nextToken + prevToken;
                }
                else {
                    String temp = prevToken;
                    prevToken = nextToken;
                    outputString = temp + ", " + nextToken;
                    nextToken = temp + nextToken;
                }
                Matcher matcher = pattern.matcher(nextToken);

                // if not, don't write
                if (!matcher.matches ())
                    continue;

                // otherwise, write
                word.set("(" + outputString.toLowerCase() + ")");
                context.write(word, one);
            }
        }
    }

    public static class WordCountReducer
            extends Reducer<Text,IntWritable,Text,IntWritable> {
        private IntWritable result = new IntWritable();

        public void reduce(Text key, Iterable<IntWritable> values,
                           Context context
        ) throws IOException, InterruptedException {
            int sum = 0;
            for (IntWritable val : values) {
                sum += val.get();
            }
            if (sum > 20) {
                result.set(sum);
                context.write(key, result);
            }
        }
    }

    public int run(String[] args) throws Exception {

        Configuration conf = new Configuration();
        Job job = Job.getInstance(conf, "word count");
        job.setJarByClass(WordCount.class);
        job.setMapperClass(WordCountMapper.class);
        job.setCombinerClass(WordCountReducer.class);
        job.setReducerClass(WordCountReducer.class);
        job.setOutputKeyClass(Text.class);
        job.setOutputValueClass(IntWritable.class);

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
INSERT INTO teste VALUES (105095, 105090);
INSERT INTO teste VALUES (105090, 105095);
INSERT INTO teste VALUES (105100, 105095);


CREATE TABLE nodes
  (
     paperid    INTEGER,
     papertitle VARCHAR (100)
  );

CREATE TABLE edges
  (
     paperid      INTEGER,
     citedpaperid INTEGER
  );

DECLARE @myVisited TABLE
  (
     paperid INTEGER,
     visited INTEGER
  );

INSERT INTO @myVisited
SELECT n.paperid,
       0
FROM   nodes n

DECLARE @totalNodesCnt INTEGER = (SELECT Count(*)
   FROM   nodes);

PRINT @totalNodesCnt

DECLARE @visitCnt INTEGER = 0;
DECLARE @startFromID INTEGER;

WHILE @visitCnt < @totalNodesCnt
  BEGIN
      DECLARE @myComponent TABLE
        (
           paperid    INTEGER,
           papertitle VARCHAR (1000)
        );

      SET @startFromID = (SELECT TOP(1) n.paperid
                          FROM   nodes n,
                                 @myVisited v1
                          WHERE  ( n.paperid = v1.paperid
                                   AND v1.visited = 0 )
                          ORDER  BY paperid)

      INSERT INTO @myComponent
      SELECT DISTINCT n.paperid,
                      n.papertitle
      FROM   nodes n
      WHERE  n.paperid = @startFromID;

      DECLARE @prev_cnt INT = 0;

      WHILE @prev_cnt < (SELECT DISTINCT Count(*)
                         FROM   @myComponent)
        BEGIN
            PRINT @prev_cnt

            SET @prev_cnt = (SELECT DISTINCT Count(*)
                             FROM   @myComponent)

            PRINT @prev_cnt

            INSERT INTO @myComponent
            SELECT DISTINCT n.paperid,
                            n.papertitle
            FROM   nodes n,
                   edges e1
                   JOIN @myComponent cc1
                     ON ( cc1.paperid = e1.paperid )
            WHERE  n.paperid = e1.citedpaperid
                   AND n.paperid NOT IN (SELECT cc3.paperid
                                         FROM   @myComponent cc3)

            INSERT INTO @myComponent
            SELECT DISTINCT n.paperid,
                            n.papertitle
            FROM   nodes n,
                   edges e2
                   JOIN @myComponent cc2
                     ON ( cc2.paperid = e2.citedpaperid )
            WHERE  n.paperid = e2.paperid
                   AND n.paperid NOT IN (SELECT cc3.paperid
                                         FROM   @myComponent cc3)
        END;

      SET @visitCnt = @visitCnt
                      + (SELECT DISTINCT Count(*)
                         FROM   @myComponent)

      UPDATE @myVisited
      SET    visited = 1
      WHERE  paperid IN (SELECT cc.paperid
                         FROM   @myComponent cc)
             AND visited = 0

      DECLARE @ccCnt INTEGER = (SELECT DISTINCT Count(*)
         FROM   @myComponent);

      WHILE @ccCnt > 4
            AND @ccCnt <= 10
        BEGIN
            SELECT *
            FROM   @myComponent

            SET @ccCnt = -1
        END

      DELETE FROM @myComponent
  END
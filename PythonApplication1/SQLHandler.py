import psycopg2

class SQLHandler(object):

    def __init__(self):
        self.cursor = self.createCursor()
        self.iteration = self.setIteration();

    # Initialize the cursor (which we can put the queries in)
    def createCursor(self):
        try:
            conn = psycopg2.connect("dbname='postgres' user='logbot' host='localhost' password='logbot'")
        except:
            print("I am unable to connect to the database")
        conn.autocommit = True
        return conn.cursor();

    # Sets this iteration to the max iteration + 1 (the current iteration)
    def setIteration(self):
        strQuery = "select max(iteration) + 1 from logs;"
        self.cursor.execute(strQuery);
        rows = self.cursor.fetchall()
        if(len(rows) == 0 or rows[0][0] is None):
            return 1;
        else:
            return rows[0][0];

    # Insert a new row into the table
    def insertRow(self, submissionid, commentid, linkstring, author, body, banned_by):
        strQuery = "insert into logs (submissionid, commentid, linkString, author, body, banned_by, datelogged, iteration) values "
        strQuery += "( '" + str(submissionid) + "', '" 
        strQuery += str(commentid) + "', '" 
        strQuery += str(linkstring) + "', '" 
        strQuery += str(author) + "', '" 
        strQuery += str(body) + "', '" 
        strQuery += str(banned_by) + "', "
        strQuery += " now(), "
        strQuery += str(self.iteration) + ");"
        return self.cursor.execute(strQuery);
     
    # check if this submissionID is already in the table
    def checkSubmissionID(self, submissionid):
        strQuery = "select 1 from logs where submissionid = '" + str(submissionid) + "';"
        self.cursor.execute(strQuery)
        rows = self.cursor.fetchall()
        return len(rows) > 0;

    # check if this submissionID/commentID combo is already in the table
    def checkCommentID(self, submissionid, commentid):
        strQuery = "select 1 from logs where submissionid = '" + str(submissionid) + "' and commentid = '" + commentid + "';"
        self.cursor.execute(strQuery)
        rows = self.cursor.fetchall()
        return len(rows) > 0;

    #Return all rows from this iteration
    def getAllFromThisIteration(self):
        strQuery = "select * from logs where iteration = " + str(self.iteration) + ";"
        self.cursor.execute(strQuery)
        return self.cleanRows(self.cursor.fetchall());

    def cleanRows(self, rows):
        returnRow = [];
        listRows = list(rows);
        for row in listRows:
            row = list(row);
            row[7] = row[7].strftime("%B %d, %Y -  %H:%M:%S");
            returnRow.append(row);
        return returnRow;
            

package tag2matlab;
import java.io.*;
import java.util.*;

/* Tag2Matlab class takes tagged-Fortran code from Escort and converts it into *
 * Matlab code.  J. Borman (2017-08-17)                                        */

public class Tag2Matlab {

    public String FILESTRING;
    public String FILELOCATION;
    public String FILENAMEEXT;
    public String FILENAME;
    public String FILEEXT;

    public static int FLAG = 0;         // Tracks if Matlab code should be commented in (1=yes, 0=no)
    public static int COUNT = 0;        // Tracks lines to be commented out (0=commented in, else=commented out)
    public static int CONT = 0;
    public static int CALL = 0;
    public static int FIRSTCHAR = 0;    // Tracks the index of the first character
    public static String FUNCNAME = "";
    public static String INITIALTEXT = "";  // Tracks the initial text from the current line
    public static String PREVTEXT = "";     // Tracks the final text from the previous line
    public static int EMPTYLINE = 0;
        
    public static int REALS = 0;    // Tracks local real declarations (1=yes, 0=no)
    public static int INTS = 0;     // Tracks local integer declarations (1=yes, 0=no)
    public static int DATA = 0;     // Tracks local data declarations (1=yes, 0=no)
    public static int COMOUT = 0;   // Tracks commented out lines (1=yes, 0=no) 
    
    public static void main(String[] args) throws FileNotFoundException, IOException {
        Tag2Matlab dummy = new Tag2Matlab();
        dummy.run(1,args[0]);
    }

    public void run(int print, String... file_location) throws FileNotFoundException, IOException{
     // print = 0       ==> create file only
     // print = 1       ==> print to screen only
     // print = 2       ==> create file and print to screen

        FILESTRING = file_location[0];

     // Find the filename
        Functions fn = new Functions();
        String[] fnArray = new String[4];
        fnArray = fn.findFileName(FILESTRING);

        FILELOCATION = fnArray[0];
        FILENAMEEXT = fnArray[1];
        FILENAME = fnArray[2];
        FILEEXT = fnArray[3];

     // Take that input and read the file by that name
        FileReader fi = new FileReader(FILESTRING);

     // Try the buffered reader for reading line by line
        BufferedReader br = new BufferedReader(fi);
        Scanner fr = new Scanner(br);

     // Initialize the .m output file
        FileOutputStream fos = null;
        BufferedWriter bw = null;
        if (print == 0 || print == 2){
            File fout = new File(FILELOCATION+FILENAME.toLowerCase()+".m");
            fos = new FileOutputStream(fout);
            bw = new BufferedWriter(new OutputStreamWriter(fos));
        }


     // Initialize text strings for the following while loop
        String lineText = "";
        String lineTextFinal = "";
        String heading = "%% THIS CODE WAS CONVERTED USING JB'S CONVERT TAG"
                + " TO MATLAB TOOL";
        String[] lineTracker = {heading,""};    // initiate line tracker
        String[] lineTracker2 = new String[2];

     // Print First Line
        if (print == 2){
            System.out.println(lineTracker[0]);
            bw.write(lineTracker[0]);
            bw.newLine();
        }
        else if (print == 0){
            bw.write(lineTracker[0]);
            bw.newLine();
        }
        else
            System.out.println(lineTracker[0]);


        Functions lineVar = new Functions();
     // Start while loop that looks for the next line and perform each of the following
     // methods on that line.
        while (fr.hasNextLine()){
            lineTracker[0] = lineTextFinal;     // text from the previous line
            lineText = fr.nextLine().toLowerCase();
            lineTracker[1] = lineText;          // text from next line
            
            PREVTEXT = lineTracker[0];      // previous line's final text
            INITIALTEXT = lineTracker[1];   // current line's initial text
            
            FIRSTCHAR = lineVar.findFirstChar(lineText);  // find location of first character
            
         // Check if the current line has no text. If so, print the line.
            if (lineText.isEmpty() || lineText.equals("\t")){
                EMPTYLINE = 1;
                COMOUT = 0;
                if (COUNT > 0){  // Force a decrement on COUNT if line is empty
                    COUNT--;
                    lineTextFinal = "%";
                }
                else{
                    lineTextFinal = lineText.replaceAll("\t","");
                }
            }
         // Check if the current line is commented out. If so, run the commentedOutLine
         // method and ignore the rest.
            else if (lineText.substring(0,1).equals("c")){
                EMPTYLINE = 0;
                COMOUT = 1;
                lineTextFinal = lineVar.commentedOutLine(lineText);
                lineTextFinal = lineVar.matlabCode(lineTextFinal);
            }
         // Run the methods
            else{
                EMPTYLINE = 0;
                COMOUT = 0;
             // Start searching methods
                lineTracker = lineVar.continuation(lineTracker);  // DON'T PUT ANY METHODS ABOVE HERE
                lineTextFinal = lineTracker[1];           // part of continuation method
                PREVTEXT = lineTracker[0];                // change prev text if cont exists

                lineTextFinal = lineVar.semiColon(lineTextFinal); // perform this method before commentedOut method (!)
                lineTextFinal = lineVar.contCommentOut(lineTextFinal);
                lineTextFinal = lineVar.powFunction(lineTextFinal);
                lineTextFinal = lineVar.booleanExpressions(lineTextFinal);
                lineTextFinal = lineVar.logFunctions(lineTextFinal);
                lineTextFinal = lineVar.varTypes(lineTextFinal);  //Added 2/26/18
                lineTextFinal = lineVar.doLoop(lineTextFinal);
                lineTextFinal = lineVar.ifThen(lineTextFinal);
                lineTextFinal = lineVar.commentedOutLine(lineTextFinal);
                lineTextFinal = lineVar.commentedOut(lineTextFinal);
                lineTextFinal = lineVar.avg(lineTextFinal);     // Must be before the call method
//                lineTextFinal = lineVar.zeroWorkArray(lineTextFinal); // Commented out 9/5/17
                lineTextFinal = lineVar.declarations(lineTextFinal);
                lineTextFinal = lineVar.call(lineTextFinal);
                lineTextFinal = lineVar.unknownFunction(lineTextFinal);
                lineTextFinal = lineVar.removeDoubleComments(lineTextFinal);
                lineTextFinal = lineVar.removeDoubleSemiColons(lineTextFinal);
                lineTextFinal = lineVar.ibits(lineTextFinal);
                lineTextFinal = lineVar.matlabCode(lineTextFinal);

                lineTextFinal = lineVar.removeSemiColon(lineTextFinal,"end"); // this should be the last method
                                                                 // called to remove ; after end

                lineVar.revert(lineText);
                lineVar.matlabFunctions(lineText);
            }
            
         // Write the lineTextFinal to the new .m file (remember that we are writing
         // the previous line or lineTracker[0]
            if (print == 2){
                System.out.println(lineTracker[0]);
                bw.write(lineTracker[0]);
                bw.newLine();
            }
            else if (print == 0){
                bw.write(lineTracker[0]);
                bw.newLine();
            }
            else
                System.out.println(lineTracker[0]);

        }

        // Write the final line using lineTextFinal
        lineTextFinal = lineVar.finalEnd(lineTextFinal);

        if (print == 2){
            System.out.println(lineTextFinal);
            bw.write(lineTextFinal);
            bw.close();
        }
        else if (print == 0){
            bw.write(lineTextFinal);
            bw.close();
        }
        else
            System.out.println(lineTextFinal);


    }

}


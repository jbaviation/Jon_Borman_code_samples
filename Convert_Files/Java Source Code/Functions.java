package tag2matlab;

public class Functions extends Tag2Matlab {
  /* GENERAL MATLAB FUNCTIONS -------------------------------------------------- */
     // Continuation of a line (& to ...)
     public String[] continuation(String[] input){
         String[] output = new String[2];
         boolean check = input[1].length() > 6; // Check the length
         if (check &&
            (input[1].substring(5,6).contains("&") || input[1].substring(5,6).contains("*"))){
             // remove the semicolon and add "..."
             output[0] = input[0].replace(";"," ") + "...";
             output[1] = "      " + input[1].substring(6);
             CONT = 1;
         }
         else
             output = input;             
         return output;
     }

     // Keep MATLAB from writing to the console (treat commented lines separate)
     public String semiColon(String input){
         String output = "";
         if (input.contains("!!") || input.contains("!"))
             output = input.replace(" !",";!");
         else
             output = input + ";";  
         return output;
     }

 /* COMMENTING OUT FUNCTIONS -------------------------------------------------- */
    // Commented out line "C"
    public String commentedOutLine(String input){
        String output = "";
        String firstLetter = "" + input.charAt(0);

        if (firstLetter.equalsIgnoreCase("c")){
            COMOUT = 1;
            output = "%" + input.substring(1);
        }
        else
            output = input;
        return output;
    }

    // Commented out "!"
    public String commentedOut(String input){
        String output = input.replace("!","%");
        return output;
    }
    
    // Check for continuation of commented out info
    public String contCommentOut(String input){
        String output = "";
        String firstLetterPrev = "";
        if (PREVTEXT.length() > 0)
            firstLetterPrev = "" + PREVTEXT.charAt(0);
        else
            firstLetterPrev = " ";
        boolean comoutline = firstLetterPrev.equals("%");
        boolean comoutpart = PREVTEXT.contains("%");
        boolean comout = comoutline || comoutpart;
        boolean cont = PREVTEXT.contains("...");
        
    //  Set global commented line out variables
        if (comout)
            COMOUT = 1;
        else
            COMOUT = 0;
        
    //  Set global continuation line variable
        if (cont)
            CONT = 1;
        else
            CONT = 0;
    
        if (COMOUT == 1 && CONT == 1){  // if the previous line was commented out and has a continuation 
            COMOUT = 1;
            output = "%" + input.substring(1);
        }
        else
            output = input;
        
        return output;
    }

    // Comment out lines with functions that don't translate to MATLAB
    public String unknownFunction(String input){
        String output = "";
        String inRS = removeSpaces(input);
        boolean case1 = input.contains("lib$");
        boolean case2 = input.contains("open(") || input.contains("close(") ||
                input.contains("open (") || input.contains("close (");
        boolean case3 = input.contains("write(") || input.contains("write (");
        boolean case4 = input.contains("type*");
        boolean case5 = input.contains("varmsq(") || input.contains("varmsq (");
        boolean case6 = input.contains("read(") || input.contains("read (");
        boolean case7 = inRS.contains("nftag$");
        if (case1 || case2 || case3 || case4 || case5 || case6 || case7){
            // Add any additional cases to comment out here
            output = "%" + input.substring(1);
        }
        else if (input.contains(" goto ")){  // Comment out the goto reference
            int locGoTo = input.indexOf("goto");
            output = input.substring(0, locGoTo) + " %" + input.substring(locGoTo);
        }
//        else if (input.length() >= 5 && isNumeric(input.substring(0,5))){  // Comment out the goto location
//            output = "%" + input.substring(0);
//        }
        else
            output = input;

        return output;
    }

  /* LOGICAL FUNCTIONS --------------------------------------------------------- */
     // Do loops (declaration and end)
     public String doLoop(String input){
         String output = "";
         boolean findDo = input.contains(" do(") || input.contains(" do ");
         boolean findWhile = input.contains("while");
         if (input.length() < 9){
             output = input;
         }
         else if (input.substring(6).contains("end do"))
             output = input.replace("end do","end");          // End
         else if (input.substring(6).contains("enddo")){
             output = input.replace("enddo;","end");          // End
             output = output.replace("enddo","end");
         }
         else if (findDo){
             output = removeSemiColon(input,"do");
             output = output.replace(",",":");
             if (findWhile){
                 output = output.replace("while","");
                 output = output.replace("do","while");
             }
             else{
                 output = output.replace("do", "for");
             }
             
             
         }
         else
             output = input;
         return output;
     }

     public String ifThen(String input){
         String output = "";
         boolean findIf = input.contains(" if(") || input.contains(" if ");
         if (input.length() < 9){
             output = input;
         }
         else if (input.substring(6).contains("end if"))
             output = input.replace("end if","end");         // End
         else if (input.substring(6).contains("endif"))
             output = input.replace("endif","end");          // End
         else if (input.substring(6).contains("else")){
             output = removeSemiColon(input,"else");
             output = output.replace("else if", "elseif");
             output = output.replace("then","");
         }
         // Declaration
  //        else if ((sub5_8) || (sub7_10) || (sub9_12) || (sub11_14) || (sub13_16)){
         else if (findIf){
             output = removeSemiColon(input,"if");
             output = output.replace("then", "");
         }
         else
             output = input;
         return output;
     }

 /* MATH FUNCTIONS------------------------------------------------------------- */
    // Power function
    public String powFunction(String input){
        String output = input.replace("**","^");
        return output;
    }

    // Boolean expressions
    public String booleanExpressions(String input){
        String output = input.replace(".eq.","==");
        output = output.replace(".gt.",">");
        output = output.replace(".ge.",">=");
        output = output.replace(".lt.","<");
        output = output.replace(".le.","<=");
        output = output.replace(".ne.","~=");

        output = output.replace(".true.","true");
        output = output.replace(".false.","false");

        output = output.replace(".and.","&&");
        output = output.replace(".or.","||");
        output = output.replace(".not.","~");
        return output;
    }

    // Logarithmic functions
    public String logFunctions(String input){
        String output = input.replace("alog","log");
        return output;
    }
    
    // Converting variable types
    public String varTypes(String input){
        String output = input;
        String input_ns = removeSpaces(input);
        
        if (input_ns.contains("int(")){
            output = output.replace("int(","floor(");
            output = output.replace("int (","floor(");
        }
        else if (input_ns.contains("float(")){
            output = output.replace("float(","(");
            output = output.replace("float (","(");
        }
        
        return output;
    }


/* SUBROUTINE TYPE FUNCTIONS -------------------------------------------------- */
    // Call function
    public String call(String input){
        input = input.toLowerCase();
        String output;
        if (input.contains(" call ")){
            output = input.replace(" call "," ");
            output = output.replace(".tag", "");
            output = output.replace(".for", "");
            output = output.replace(".f90", "");
            output = output.replace(".f95", "");
            output = output.replace(".f",   "");
        }
        else
            output = input;
        return output;
    }

    public String ibits(String input){
        String output = "";
        boolean testIbits = input.contains("ibits(") || input.contains("ibits ");
        if (testIbits){
            int findIbits = input.indexOf("ibits");
            output = input.substring(0,findIbits) + "1;";
        }
        else
            output = input;
        return output;
    }

    // Reals, include, subroutine, return and final end statement
    public String declarations(String input){
        input = input.toLowerCase();
        
        // Evaluate input up to where comment begins
        String input_eval = codeB4comment(input,"%");
    
        String output = input;
        
        int trackSwitch = 0;
//        boolean cond1 = input.length() > 10;
//        boolean cond2 = cond1 && input.substring(5,10).contains(" real");
//        boolean cond3 = input.contains("/");
//        boolean cond4 = input.contains("=");
//        boolean cond5 = input.length()>13 && input.contains(" integer");
//        boolean cond6 = cond1 && input.contains(" data");
//        boolean cond7 = input.length() > 13;
//        boolean cond8 = cond7 && (input.substring(5).contains(" common ") || input.substring(5).contains(" common/"));
        
        boolean cond1 = input_eval.length() > 10;
        boolean cond2 = cond1 && input_eval.substring(5,10).contains(" real");
        boolean cond3 = input_eval.contains("/");
        boolean cond4 = input_eval.contains("=");
        boolean cond5 = input_eval.length()>13 && input_eval.contains(" integer");
        boolean cond6 = cond1 && input_eval.contains(" data");
        boolean cond7 = input_eval.length() > 13;
        boolean cond8 = cond7 && (input_eval.substring(5).contains(" common ") || input_eval.substring(5).contains(" common/"));
        
        if (cond2){  // Real declaration exists
            if (!(cond3 || cond4)){  // First reals option
                trackSwitch = 1;
                output = "%" + input.substring(1);                
            }
            else{ // change reals
                trackSwitch = 1;
                REALS = 1;
                for (int i=10; i<output.length()-1; i++){
                    if (output.substring(i,i+1).equals("/")){
                        output = output.substring(0,i)+"=["+output.substring(i+1);
                        break;
                    }
                }
                output = output.replace("real","");
                if (output.contains("/")){
                    output = output.replace("/", "]");
                    REALS = 0;
                }
                if (output.contains("(") && output.contains(")")){
                    int locParen1 = output.indexOf("(");
                    int locParen2 = output.indexOf(")");
                    String beforeParen = output.substring(0,locParen1);
                    String afterParen = output.substring(locParen2+1);
                    output = beforeParen + afterParen;
                }
            }
        }

        else if (cond5){ // Integer declaration exists
            if (!(cond3 || cond4)){  // First integer option
                trackSwitch = 1;
                output = "%" + input.substring(1);                
            }
            else {
                trackSwitch = 1;
                INTS = 1;
                for (int i=10; i<output.length()-1; i++){
                    if (output.substring(i,i+1).equals("/")){
                        output = output.substring(0,i)+"=["+output.substring(i+1);
                        break;
                    }
                }
                output = output.replace("integer","");
                if (output.contains("/")){
                    output = output.replace("/", "]");
                    INTS = 0;
                }
                if (output.contains("(") && output.contains(")")){
                    int locParen1 = output.indexOf("(");
                    int locParen2 = output.indexOf(")");
                    String beforeParen = output.substring(0,locParen1);
                    String afterParen = output.substring(locParen2+1);
                    output = beforeParen + afterParen;
                }
            }
        }
        else if (cond6){ // Data declaration exists
            if (!(cond3 || cond4)){  // First data option
                trackSwitch = 1;
                output = "%" + input.substring(1);                
            }
            else {
                trackSwitch = 1;
                DATA = 1;
                for (int i=10; i<output.length()-1; i++){
                    if (output.substring(i,i+1).equals("/")){
                        output = output.substring(0,i)+"=["+output.substring(i+1);
                        break;
                    }
                }
                output = output.replace("data","");
                if (output.contains("/")){
                    output = output.replace("/", "]");
                    DATA = 0;
                }
                if (output.contains("(") && output.contains(")")){
                    int locParen1 = output.indexOf("(");
                    int locParen2 = output.indexOf(")");
                    String beforeParen = output.substring(0,locParen1);
                    String afterParen = output.substring(locParen2+1);
                    output = beforeParen + afterParen;
                }
            }
        }
        else if (CONT == 1 && REALS == 1 && cond3){ //continuation of real call
            output = output.replace("/","];");
            REALS = 0;
        }
        else if (CONT == 1 && DATA == 1 && cond3){ //continuation of data call
            output = output.replace("/","];");
            REALS = 0;
        }
        else if ((input_eval.length() > 13) && (input_eval.substring(5).contains(" include "))){  // change include
            trackSwitch = 1;
            output = "%" + input.substring(1);
        }
        else if ((input_eval.length() > 16) && (input_eval.substring(5).contains(" subroutine "))){  // change subroutine
            if (input.contains("("))
            trackSwitch = 1;
            output = "%" + input.substring(1);
        }
        else if ((input_eval.length() > 6) && (input_eval.substring(5).contains(" return;"))){       // change returns
            trackSwitch = 1;
            output = "%" + input.substring(1);
        }
        else if ((input_eval.length() > 6) && (input_eval.substring(5).contains(" character"))){       // change character
            trackSwitch = 1;
            output = "%" + input.substring(1);
        }
        else if ((input_eval.length() > 6) && (input_eval.substring(5).contains(" dimension"))){       // change dimension
            trackSwitch = 1;
            output = "%" + input.substring(1);
        }
        else if ((input_eval.length() > 6) && (input_eval.substring(5).contains(" equivalence"))){    // change equivalence
            trackSwitch = 1;
            output = "%" + input.substring(1);
        }
        else if ((input_eval.length() > 6) && (input_eval.substring(5).contains(" parameter "))){    // change parameter
            trackSwitch = 1;
            output = "%" + input.substring(1);
        }
        else if ((input_eval.length() > 6) && (input_eval.substring(5).contains(" byte "))){       // change byte
            trackSwitch = 1;
            output = "%" + input.substring(1);
        }
        else if (cond7 && cond8){   // change common call
            trackSwitch = 1;
            output = "%" + input.substring(1);
        }
        else if ((input_eval.length() > 13) && (input_eval.substring(5).contains(" integer "))){  // change include
            trackSwitch = 1;
            output = "%" + input.substring(1);
        }
        else if (input_eval.contains("type *") || input_eval.contains("type*")){  // type statement
            trackSwitch = 1;
            output = "%" + input.substring(1);
        }
        else if (input_eval.contains(" exit ") || input_eval.contains(" exit\r") || input_eval.contains(" exit;")){  // exit
            trackSwitch = 1;
            output = input.replace("exit","break");
        }
        else if ((input_eval.length() > 6) && ((input_eval.substring(6).contains("end  ")) ||       // change final end
                (input_eval.substring(6).contains("end\r")) || (input_eval.substring(6).contains("end \r")))){
            trackSwitch = 1;
            output = "%" + input.substring(1);
        }
        else {
            output = input;
        }
// Copied Code
//        else if ((input.length() > 13) && (input.substring(5).contains(" include "))){  // change include
//            trackSwitch = 1;
//            output = "%" + input.substring(1);
//        }
//        else if ((input.length() > 16) && (input.substring(5).contains(" subroutine "))){  // change subroutine
//            if (input.contains("("))
//            trackSwitch = 1;
//            output = "%" + input.substring(1);
//        }
//        else if ((input.length() > 6) && (input.substring(5).contains(" return;"))){       // change returns
//            trackSwitch = 1;
//            output = "%" + input.substring(1);
//        }
//        else if ((input.length() > 6) && (input.substring(5).contains(" character"))){       // change character
//            trackSwitch = 1;
//            output = "%" + input.substring(1);
//        }
//        else if ((input.length() > 6) && (input.substring(5).contains(" equivalence"))){    // change equivalence
//            trackSwitch = 1;
//            output = "%" + input.substring(1);
//        }
//        else if ((input.length() > 6) && (input.substring(5).contains(" parameter "))){    // change parameter
//            trackSwitch = 1;
//            output = "%" + input.substring(1);
//        }
//        else if ((input.length() > 6) && (input.substring(5).contains(" byte "))){       // change byte
//            trackSwitch = 1;
//            output = "%" + input.substring(1);
//        }
//        else if (cond7 && cond8){   // change common call
//            trackSwitch = 1;
//            output = "%" + input.substring(1);
//        }
//        else if ((input.length() > 13) && (input.substring(5).contains(" integer "))){  // change include
//            trackSwitch = 1;
//            output = "%" + input.substring(1);
//        }
//        else if (input.contains("type *") || input.contains("type*")){  // type statement
//            trackSwitch = 1;
//            output = "%" + input.substring(1);
//        }
//        else if (input.contains(" exit ") || input.contains(" exit\r") || input.contains(" exit;")){  // exit
//            trackSwitch = 1;
//            output = input.replace("exit","break");
//        }
//        else if ((input.length() > 6) && ((input.substring(6).contains("end  ")) ||       // change final end
//                (input.substring(6).contains("end\r")) || (input.substring(6).contains("end \r")))){
//            trackSwitch = 1;
//            output = "%" + input.substring(1);
//        }
//        else {
//            output = input;
//        }

        if (trackSwitch == 1){
            output = output.replaceAll("/","");     // find any errant slashes
        }
        return output;
    }
    
    public String finalEnd(String input){
        // Only call this method before the final line evaluation!!
        // this forces the last end to be commented out
        String output = input.replace("end","%end");
        return output;
    }

    // Average calculation
    public String avg(String input){
        String output = "";
        boolean check1 = input.contains("call std$");
        boolean check2 = input.contains("call avg$");
        if (check1 || check2){
            int locVarParen = 0;
            int locFuncParen = 0;
            int numCommas = 0;
            int stArray = 1;

            if (input.contains("("))
                locFuncParen = input.indexOf("(") + 1;
            else
                return input;
        
         // Find variable names 
            numCommas = delimeterCounter(input,",");// Count number of commas for size of array
            String[] insideParens = new String[numCommas+1];
            insideParens = delimeterParse(input,locFuncParen);
            String varNameOut = insideParens[2];
            String varNameIn  = insideParens[1];
            
            if (varNameIn.contains("(")){
                int locParenEnd = varNameIn.indexOf(")");
                locVarParen = varNameIn.indexOf("(");
                String numVarIn = varNameIn.substring(locVarParen+1,locParenEnd);
                stArray = Integer.parseInt(numVarIn);   // Find starting array position
                varNameIn = varNameIn.substring(0,locVarParen);
            }
            
         // Find number of elements in array
            String numArray = "";
            try{
                int numArrayInt = Integer.parseInt(removeSpaces(insideParens[0]));
                numArrayInt = numArrayInt + (stArray-1);
                numArray = Integer.toString(numArrayInt);
            } catch (Exception e){
                numArray = removeSpaces(insideParens[0]);
            }

            
         // Set initial space
            String space = repeater(" ",FIRSTCHAR);
//            for (int j=0; j<FIRSTCHAR; j++){
//                space = space + " ";
//            }
            if (check1){ // calculate the mean, max, min, std
                output = space +
                    varNameOut+" = mean("+varNameIn+"("+stArray+":"+numArray+"));"+
                    insideParens[4]+"=max("+varNameIn+"("+stArray+":"+numArray+"));"+
                    insideParens[3]+"=min("+varNameIn+"("+stArray+":"+numArray+"));"+
                    insideParens[5]+"=std("+varNameIn+"("+stArray+":"+numArray+"));";
            }
            else{    // calculate the mean
                output = space +
                    varNameOut+" = mean("+varNameIn+"("+stArray+":"+numArray+"));";          
            }
                
        }
        else
            output = input;
        return output;
    }

    // Transform Fortran Subroutines that become Matlab Functions
    public void matlabFunctions(String input){
        int locSubroutine; int locCall;
        int locParen;

        if (input.contains("subroutine") && input.contains("(")){
            locSubroutine = input.indexOf("subroutine") + 10;
            locParen = input.indexOf("(");
            FUNCNAME = input.substring(locSubroutine,locParen);
        }
        if (input.contains("call") && input.contains("(")){
//        if (CALL == 1 && input.length()){
            locCall = input.indexOf("call") + 4;
            locParen = input.indexOf("(");
            FUNCNAME = removeSpaces(input.substring(locCall,locParen));
        }
       
    }
    
    // Recognize the call for Matlab code to be used instead of the next line
    public String matlabCode(String input){
        String output = "";
        int numLines = 0;
        boolean matlabID = input.contains("@matlab");
        if (matlabID){  // if a commented line contains the text use this line instead of the next
            FLAG = 1;
            boolean broke = false;
            String firstLetter = "" + input.charAt(0);
            int locMatlab = input.indexOf("@matlab");
            
        //  Initialize loop that looks for the number after @matlab
            String numLinesStr = "";
            int i = locMatlab + 7;
            String c = input.substring(i,i+1);
            while (!c.equals(" ")){
//            while (!isNumeric(c)){
                if (isNumeric(c))
                    numLinesStr = numLinesStr + c;    // if the space is numeric add it
                i++;  // move to the next space
                try{
                    c = input.substring(i,i+1); // check the character at the next space
                } catch (StringIndexOutOfBoundsException e) { 
                    broke = true;
                    break;
                }
            }
        //  Check if numLinesStr is numeric
        //  If so, convert it to an integer, if not default to 1
            if (isNumeric(numLinesStr))
                numLines = Integer.parseInt(removeSpaces(numLinesStr));
            else
                numLines = 1;
            COUNT = numLines;   // update the global variable that tracks how many lines to com out
            
            int locEndID = i + 1;
            if (firstLetter.equals("%")){ // comment this line in
                if (broke)
                    output = "% @matlab"+numLines+": commenting the following "+numLines+" lines out.";
                else
                    output = repeater(" ",FIRSTCHAR) + input.substring(locEndID);
            }
        }
        else if (COUNT > 0){  // when COUNT>0 the next line is commented out
            FLAG = 0;
            COUNT--;
            output = "%" + input.substring(1);
        }
        else{
            FLAG = 0;
            COUNT = 0;
            output = input;
        }
        
        return output;
    }
    

/* ADMINISTRATIVE CHANGES ----------------------------------------------------- */
    public String[] findFileName(String input){
        String input_lower = input.toLowerCase();  // input_lower for searching purposes, use input for filename
        String[] output = new String[4];
        String sep = "";
        int lastSep = 0;

        if (input_lower.contains(".tag") || input_lower.contains(".for")){
            if (input_lower.contains("/")){
                sep = "/";
            }
            else if (input_lower.contains("\\")){
                sep = "\\";
            }
            else{
                System.err.println("Error: your file location uses a format that is not recognized by this program");
            }

            lastSep = input.lastIndexOf(sep);
            output[0] = input.substring(0,lastSep+1);                   // File Location
            output[1] = input.substring(lastSep+1,input.length());      // File Name + Extension

        }
        else
            System.err.println("Error: this program only accepts .tag or .for extensions");

        int locDot = input.lastIndexOf(".");
        output[2] = input.substring(lastSep+1,locDot);                  // File Name
        output[3] = input.substring(locDot,input.length());             // File Extension

        return output;      // 4 elements include [File Location, File Name + Extension, File Name, File Extension]
    }

    public boolean isNumeric(String inputData) {
        return inputData.matches("[-+]?\\d+(\\.\\d+)?");
    }

/* REPEATABLE CALLS ----------------------------------------------------------- */
    // Remove semicolon for lines with logical commands
    public String removeSemiColon(String input, String criteria){
        String output = "";
        if (input.contains(criteria))
            output = input.replace(";", "");
        else
            output = input;
        return output;
    }
    public String removeSpaces(String input){
        String output = input.replaceAll("\\s+","");
        return output;
    }
    
    // Delimiter Counter; counts the number of a given symbol
    public int delimeterCounter(String input, String delimeter){
        int output = input.length() - input.replace(delimeter, "").length();
        return output;
    }
    
    // Parses out values contained within a comma-separated call
    public String[] delimeterParse(String input, int startPosition){
        String inputSub = input.substring(startPosition);
        int commaCountTot = delimeterCounter(inputSub, ",");
        
        String[] output = new String[commaCountTot+1];
        int[] locComma = new int[commaCountTot];
        
        boolean parenExists = input.contains(")");
        
        // Initialize variables for finding the location of each comma
        int commaCount = 0;
        for (int j=0; j<inputSub.length(); j++){ // run thru text
            String Charat = "" + inputSub.charAt(j);
            if (Charat.equals(",")){
                locComma[commaCount] = j;
                commaCount++;
            }
        }
        // Find last parenthesis
        int lastParen = -1;
        if (parenExists)
            lastParen = inputSub.lastIndexOf(")");
        
        // Write text for each comma-separated segment
        for (int i=0; i<=output.length-1; i++){
            int textBegin;
            int textEnd;
            
            // Beginning Text
            if (i == 0)
                textBegin = 0;
            else
                textBegin = locComma[i-1] + 1;
            // Ending Text
            if (i == output.length-1)
                textEnd = lastParen;
            else
                textEnd = locComma[i];
            
            output[i] = removeSpaces(inputSub.substring(textBegin,textEnd));
        }
            
        return output;

    }
    
    // Find location of first non-blank character
    public int findFirstChar(String input){
        int output = 0;
        String Charat = " ";
        int i=0;
        boolean emptyLine = input.isEmpty();
        boolean commentOut = !emptyLine && input.substring(0,1).equals("c");
        if (commentOut){ // if line is commented out skip the 'c'
            input = " " + input.substring(1);
        }
        boolean containsText = input.trim().length() > 0;
        
        if (!emptyLine && containsText){  // as long as the line is not empty and contains text
            while (Charat.equals(" ")){
                Charat = "" + input.charAt(i);
                i++;
            }
            output = i-1;
        }
        return output;
    }
    
    // Generates a series of text all with the same letter, character, symbol or space
    public String repeater(String toRepeat, int howManyTimes){
        String output = "";
        if (howManyTimes > 0){
            for (int i=0; i<howManyTimes; i++){
                output = output + toRepeat;
            }
        }
        else
            output = toRepeat;
        return output;
    }
    
    // Executable code before a comment
    public String codeB4comment(String input,String commentOutSymbol){
        String output = input;
        if (input.contains(commentOutSymbol)){
            for (int i=0; i<input.length()-1; i++){
                if (input.substring(i,i+1).equals(commentOutSymbol)){
                    output = input.substring(0,i);
                    break;
                }
            }            
        }
        return output;
    }

/* UNDO UNNECESSARY PROGRAM MODIFICATIONS ------------------------------------- */
    public String removeDoubleComments(String input){
        String output = input.replaceAll("%%","%");
        return output;
    }
    
    public String removeDoubleSemiColons(String input){
        String output = input.replaceAll(";;",";");
        return output;

    }

/* REFPROP RELATED CHANGES ---------------------------------------------------- */

    
/* CHANGE GLOBAL VARIABLES BACK ----------------------------------------------- */
    public void revert(String input){
        if (CONT == 1 && !(input.contains("&") || input.contains("*")))
            CONT = 0;
    }
    
    
    
}


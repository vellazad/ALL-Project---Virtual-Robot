package algorithmsproject;


public class WordStoreImp implements WordStore
{
    int findIndex;
    int length;  // Initial number of words
    int currentIndex;
    boolean reached;  /* Used to ensure array is only mergesorted once 
    all words have been added and not before*/
    String[] wordArray;  // Array that stores the words
        
    
    public WordStoreImp(int x)
    {
        length = x;
        wordArray = new String[length];
        currentIndex = 0;
        reached = false;
        findIndex = -1;
    }

    
    public void add (String word)
    {
        /**
         * Takes a String as input and adds it to the WordStore.
         * 
         * @param add the word to be added
         */
        if (currentIndex == length - 1)  // Ensures array won't be mergesorted until all initial words have been added
            reached = true;
        if (currentIndex < length)  // Avoids creating new array if array has space for more words
        {
            wordArray[currentIndex] = word;
            currentIndex++;
        }
        else
        {
            String[] newArray = new String[length + 1];  // Creates array to replace the old one if no space left
            for (int i = 0; i < length; i++)
                newArray[i] = wordArray[i];  // Copies the words of the original array into the new one
            newArray[length] = word;  // Adds the new word to the array
            wordArray = newArray;
            length++;  // Updates the value for the size of the word store
        }
        if (reached == true)
            wordArray = mergeSort(wordArray);
    }
    
    
    public int count (String word)
    {
        /**
         * Takes a String as input and returns number of times it occurs
         * in the WordStore.
         * 
         * @param word the word to be counted
         */
        int countSoFar = 0;
        binarySearch(wordArray, word, 0, wordArray.length); // Sets findIndex to index of word, or -1 if word not found
        if (findIndex == -1)  // If word not found return 0
            return 0;
        while (true)  // Starts at occurrence of word and goes back through sorted array to find first occurrence 
        {
            if (findIndex == 0)  // If at beginning of array, don't go back
                break;
            else if (wordArray[findIndex - 1].compareTo(word) == 0)
                findIndex = findIndex - 1;
            else
                break;
        }
        while (true)  // Count forward until next word isn't our word
        {
            if (findIndex == wordArray.length)  // If at end of array, stop
                break;
            if (wordArray[findIndex].compareTo(word) == 0)
            {
                countSoFar = countSoFar + 1;
                findIndex = findIndex + 1;
            }
            else
                break;
        }
        return countSoFar;
    }
    
    
    public void remove (String word)
    {
        /**
         * Takes a string as input and removes it from the WordStore.  
         * Leaves unchanged if the word doesn't occur.
         * 
         * @param word the word to be removed
         */
        binarySearch(wordArray, word, 0, wordArray.length);
        if (findIndex == - 1)  // If word not found, leave array unchanged
            return;
        else
        {
            int i = 0;
            String[] newArray = new String[wordArray.length - 1];
            for (; i < findIndex; i++)  // Copy elements into new array up until (but not including) word to be removed
                newArray[i] = wordArray[i];
            for (; i < newArray.length; i++)  // Continue copying, skipping word to be removed
                newArray[i] = wordArray[i + 1];
            wordArray = newArray;
            length = length - 1;
            currentIndex = currentIndex - 1;
        }        
    }
    
    private static String[] mergeSort (String[] arr)
    {
        /**
         * Takes String array as input and returns alphabetically sorted array.
         * 
         * @param arr array to be sorted
         */
        int i = 0;
        int length = arr.length;
        
        if (length > 1)
        {
            int middle = length/2;
            
            // Splits array in two halfs
            String[] half1 = new String[middle];
            String[] half2 = new String[length - middle];        
            for (; i < middle; i++)
                half1[i] = arr[i];
            for (; i < length; i++)
                half2[i - middle] = arr[i];
            
            half1 = mergeSort(half1);
            half2 = mergeSort(half2);
            
            // Merges halfs
            String[] mArray = new String[arr.length];
            int j = 0;
            int k = 0;
            for(i = 0; j<half1.length && k<half2.length; i++)
            {
                if(half1[j].compareTo(half2[k])<0)  // Compares elements of first half to second half and merges them into new array
                {
                    mArray[i]=half1[j];
                    j++;
                }
                else
                {
                    mArray[i]=half2[k];
                    k++;
                }
            }
            for(; j<half1.length; i++, j++)  // Copies remaining elements into new array
                mArray[i]=half1[j];
            for(; k<half2.length; i++, k++)
                mArray[i]=half2[k];
            return mArray;            
        }
        else  // If array has one element, return same array
        {
            String[] xArray = new String[1];
            xArray[0] = arr[0];
            return xArray;
        }       
    }
    
    private void binarySearch (String[] arr, String str, int start, int end)
    {
        /**
         * Takes an array, a word and a start and end point to look for that word
         * within that range in the array.  Sets class variable findIndex to the 
         * index of the word or to -1 if not found.
         * 
         * @param arr the array within which to look for the word
         * @param str the word to be found
         * @param start the bottom index of the range within which to look for the word
         * @param end the top index of the range within which to look for the word
         */
        int middle = (start + end)/2;
        
        if (end - start == 1 && arr[middle].compareTo(str) != 0)  // If not found, set findIndex to -1
            findIndex = -1;
        else
        {
            if (str.compareTo(arr[middle]) == 0)
                findIndex = middle;
            else if (arr[middle].compareTo(str)>0)  // If middle element is greater than word, look in bottom half
                binarySearch(arr, str, 0, middle);
            else if (arr[middle].compareTo(str)<0)  // If middle element is smaller than word, look in top half
                binarySearch(arr, str, middle, end);
        }      
    }   
}

test

import java.util.*;
void testAdd ()
    {
        Scanner input = new Scanner(System.in);
        WordGen.initialise(input);
        System.out.print("Enter the number of words you wish to add: ");
        int n = input.nextInt();
        WordStore words = new WordStoreImp(n);
        long time1,time2;
        time1 = new Date().getTime();
        System.out.println(time1);
        for(int i=0; i<n; i++)
            words.add(WordGen.make());
        time2 = new Date().getTime();
        System.out.println(time2);
        System.out.println("Time taken to add " + n + " words = " + (time2-time1) + " ms");
    }

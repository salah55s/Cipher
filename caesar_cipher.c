#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <math.h>

char s[500];
int Counter = 0;
int shft = 0;
char outStrng[500];
int Diff = 0;

int main()
{
    printf("Enter string to be Encrypted By Caeser Enctryption:\n");
    gets(s);

    printf("Enter the Number of Shift From 1--> 25\n");
    scanf("%d", &shft);

    int n = strlen(s);

    for (Counter = 0; Counter < n; Counter++)
    {
        char c = s[Counter];

        if (c >= 'A' && c <= 'Z')
        {
            int Diff = 'Z' - c;

            if (Diff > shft)
            {
                outStrng[Counter] = c + shft;
            }
            else if (Diff < shft)
            {
                int Newshft;
                Newshft = shft - 26;
                outStrng[Counter] = c + Newshft;
            }
            else
            {
                outStrng[Counter] = c + shft;
            }
        }
        else if (c >= 'a' && c <= 'z')
        {
            int Diff = 'z' - c;

            if (Diff > shft)
            {
                outStrng[Counter] = c + shft;
            }
            else if (Diff < shft)
            {
                int Newshft;
                Newshft = shft - 26;
                outStrng[Counter] = c + Newshft;
            }
            else
            {
                outStrng[Counter] = c + shft;
            }
        }
        else
        {
            printf("Please Enter a Valid character\n");
            break;
        }
    }

    printf("The Encrypted Text is:\n");
    outStrng[n] = '\0';  
    puts(outStrng);

    return 0;
}

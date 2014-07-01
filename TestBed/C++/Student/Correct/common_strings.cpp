
#include <cmath>
#include <cstdio>
#include <vector>
#include <iostream>
#include <algorithm>

using namespace std;

int memo[5005][5005];
string s1,s2;
int n;

int max_sub_seq(int pos1, int pos2){
    if(pos1 >= n || pos2 >= n){
        return 0;
    }
    else if(memo[pos1][pos2] == -1){
        if(s1[pos1] == s2[pos2]){
            memo[pos1][pos2] = 1 + max_sub_seq(pos1+1,pos2+1);
        }
        else{
            int i1 = max_sub_seq(pos1,pos2+1);
            int i2 = max_sub_seq(pos1+1,pos2);
            memo[pos1][pos2] = i1>i2?i1:i2;
        }
    }
    return memo[pos1][pos2];
}

int main() {
    cin >> s1 >> s2;
    n = s1.length();

    int i,j;

    for(i=0;i<n;++i){
        for(j=0;j<n;++j){
            memo[i][j] = -1;
        }
    }

    cout << max_sub_seq(0,0) << endl;

    return 0;
}
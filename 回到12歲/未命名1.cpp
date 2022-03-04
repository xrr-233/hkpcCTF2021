#include <iostream>
#include <cstdio>
#include <cstring>
using namespace std;

char charlist[41] = " abcdefghijklmnopqrstuvwxyz0123456789{}_";
char string2[39] ="03vx{_ihq0xhh7svtx}t{sv180x{r";
int a[40];
int main() {
	
	memset(a, 0,sizeof(a));
	for(int i = 1; i <= 39; i++){
		while(true){
			a[i]++;
			//cout << charlist[(a[i]+18)%39+1] - '0' << ' '<<string2[i-1] - '0'<<endl;
			if(int(charlist[(a[i]+18)%39+1] - '0')==int(string2[i-1] - '0')){
				cout << charlist[a[i]];
				break;
			}
		}
		
	}
}

#include <stdint.h>
#include <stdlib.h>
int lev(const uint32_t *a,int n,const uint32_t *b,int m){
 if(n<m){const uint32_t*t=a;a=b;b=t;int q=n;n=m;m=q;}
 if(!m)return n;
 if(m<=64){uint64_t pv=~(uint64_t)0,mv=0,high=((uint64_t)1)<<(m-1);int s=m;
  for(int i=0;i<n;i++){uint64_t eq=0;for(int j=0;j<m;j++)if(a[i]==b[j])eq|=((uint64_t)1)<<j;
   uint64_t xv=eq|mv,xh=(((eq&pv)+pv)^pv)|eq,ph=mv|~(xh|pv),mh=pv&xh;
   s+=(ph&high)!=0;s-=(mh&high)!=0;ph=(ph<<1)|1;mh<<=1;pv=mh|~(xv|ph);mv=ph&xv;
  }return s;
 }
 int *p=malloc((m+1)*sizeof(int)),*q=malloc((m+1)*sizeof(int));if(!p||!q){free(p);free(q);return -1;}for(int j=0;j<=m;j++)p[j]=j;
 for(int i=1;i<=n;i++){q[0]=i;for(int j=1;j<=m;j++){int u=q[j-1]+1,v=p[j]+1,w=p[j-1]+(a[i-1]!=b[j-1]);q[j]=u<v?u:v;if(w<q[j])q[j]=w;}int*t=p;p=q;q=t;}
 int result=p[m];free(p);free(q);return result;
}

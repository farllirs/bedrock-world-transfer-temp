#include <stdint.h>
#include <stddef.h>
static uint32_t T[256]; static int init=0;
uint32_t crc32c(const unsigned char*p,size_t n){
 if(!init){for(uint32_t i=0;i<256;i++){uint32_t c=i;for(int k=0;k<8;k++)c=(c&1)?(c>>1)^0x82F63B78:c>>1;T[i]=c;}init=1;}
 uint32_t c=0xFFFFFFFF; for(size_t i=0;i<n;i++)c=T[(c^p[i])&255]^(c>>8); return c^0xFFFFFFFF;}

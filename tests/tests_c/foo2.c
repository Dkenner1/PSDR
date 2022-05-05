/* Save to a file, e.g. boilerplate.c, and then compile:
 * $ gcc test/foo2.c -o bin/foo_out bin/bladeRF_config.o -lbladeRF -lm
 * $ ./foo_out
 */
#include <libbladeRF.h>
#include "bladeRF_config.h"
#include <stdio.h>
#include<ctype.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <math.h>
#include<sys/time.h>

/* The RX and TX channels are configured independently for these parameters */
struct channel_config{
	 bladerf_channel channel;
	 unsigned int frequency;
	 unsigned int bandwidth;
	 unsigned int samplerate;
	 int gain;
} ;


/* Usage:
 * Transmit Main
 */
int main(int argc, char *argv[])
{	
	// initialize variables
	int status;
	unsigned int pulse_delay;
	struct channel_config config;
	TxConfig txc;
	get_config(&txc);
	print_TxConfig(&txc);
	while(txc.tx){
	usleep(700000);
	printf("In loop!\n");
	if(config_changed(&txc)){
		printf("Config Changed!\n");
		break;
	}
	}
	
return 0;	
}

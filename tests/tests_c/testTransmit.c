/* Save to a file, e.g. boilerplate.c, and then compile:
 * $ gcc boilerplate.c -o libbladeRF_example_boilerplate -lbladeRF
 */
#include <libbladeRF.h>
#include "config.h"
#include <stdio.h>
#include<ctype.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>



/* The RX and TX channels are configured independently for these parameters */
struct channel_config{
	 bladerf_channel channel;
	 unsigned int frequency;
	 unsigned int bandwidth;
	 unsigned int samplerate;
	 int gain;
};


int get_config(TxConfig *config){
    FILE *fp = fopen("bin/config.txt", "r+");
    if(fp==NULL)
    	return -1;
    keyValue *keys = malloc(0);
    char line[64];
    char (*formatted)[40] = malloc(64 * sizeof(*formatted));
    int i=0;
    while(fgets(line, 255, fp)){
    	if(line[0]=='#' || line[0]=='\n'){
    		memset(line, 0, 64);
    		continue;
    	}
    	keys=realloc(keys, (i + 1) * sizeof(keyValue));
    	format_entry(line, formatted[i]);
    	//split into key value pairs
    	keys[i].key = strtok(formatted[i], "=");
		keys[i].value = strtok(NULL, "=");
		i++;
		memset(line, 0, 64);
    }
    /*
	i=0;
	while(keys[i].key){
	printf("key: %s\n", keys[i++].key);
	}*/
	//printf("%d", atoi(keys[get_keyValue("freq", keys)].value));

    config->freq=atoi(keys[get_keyValue("freq", keys)].value);
    config->bandwidth=atoi(keys[get_keyValue("bandwidth", keys)].value);
    config->num_samples=atoi(keys[get_keyValue("num_samples", keys)].value);
    
    config->pwr=atof(keys[get_keyValue("pwr", keys)].value);
    config->duty_cycle=atof(keys[get_keyValue("duty_cycle", keys)].value);
    

    if(strcmp(keys[get_keyValue("channel_mode", keys)].value, "mimo"))
    	config->c_mode=MIMO;
	else
    	config->c_mode=SINGLE; 
    	
    if(!strcmp(keys[get_keyValue("tx_mode", keys)].value, "pulse"))
    	config->t_mode=PULSE;
    else
    	config->t_mode=CONTINUOUS;    	
	
    if(atoi(keys[get_keyValue("tx", keys)].value)==ON)
    	config->tx=ON;
    else
    	config->tx=OFF; 

    if(atoi(keys[get_keyValue("channel", keys)].value) == 2)
    	config->channel=2;
    else
    	config->channel=1; 

    free(keys);
    free(formatted);
    fclose(fp);
	return 0;
};

// Return index of keyvalue
// Hashtable would be more elegant solution
int get_keyValue(char *str, keyValue *list){
    int i=0;
    while(list[i].key){
    	if(!strcmp(list[i].key, str))
    		return i;    	
    	i++;
    }
    return -1;
};


/* format_entry
 * Function strips configuration file entry and formats 
 * it so that it can be easily parsed
 * Inputs:
 * str -> string to be parsed
 * fstr -> output formatted string 
*/
int format_entry(char *str, char *fstr){
	while(*str){
	char c=*str++;
	if(c==' ')
		continue;
	if(c>='A' && c<='Z')
		c+=32; 
	*fstr=c;
	*fstr++;	
	}
}


/*
* produce_samples
* Inputs: 
	pwr: float representation of amplitude as a percentage (0-100 inclusive)
	samples: pointer to an interger array of samples
	num_samples: determines how many samples are to be made
*/
int produce_samples(float pwr, int16_t *samples, unsigned int num_samples)
{
    int16_t steps=2047; 
    int16_t inphase, quadrature;
    inphase=quadrature=2047*pwr/100;
    
    for (int i = 0; i < 2 * num_samples; i += 2) {
        samples[i]     = inphase;
        samples[i + 1] = quadrature;
    }
}
/*
configure_channel function pulled from bladeRF example transmit
*/
int configure_channel(struct bladerf *dev, struct channel_config *c)
{
	 int status;
	 status = bladerf_set_frequency(dev, c->channel, c->frequency);
	 if (status != 0) {
		 fprintf(stderr, "Failed to set frequency = %u: %s\n", c->frequency,
		 bladerf_strerror(status));
		 return status;
 	}
	 status = bladerf_set_sample_rate(dev, c->channel, c->samplerate, NULL);
	 if (status != 0) {
		 fprintf(stderr, "Failed to set samplerate = %u: %s\n", c->samplerate,
		 bladerf_strerror(status));
		 return status;
	 }
	 
	 status = bladerf_set_bandwidth(dev, c->channel, c->bandwidth, NULL);
	 if (status != 0) {
		 fprintf(stderr, "Failed to set bandwidth = %u: %s\n", c->bandwidth,
		 bladerf_strerror(status));
		 return status;
	 }
	 status = bladerf_set_gain(dev, c->channel, c->gain);
	 if (status != 0) {
		 fprintf(stderr, "Failed to set gain: %s\n", bladerf_strerror(status));
		 return status;
	 }
	 return status;
}
/* Usage:
 * Transmit Main
 */
int main(int argc, char *argv[])
{
	
	// initialize variables
	int status;
	struct channel_config config;
	struct bladerf *dev = NULL;
	struct bladerf_devinfo dev_info;
	TxConfig txc;
	/* Initilize the device
	bladerf_init_devinfo(&dev_info);
	/* Request a device with the provided serial number.
	* Invalid strings should simply fail to match a device. */
	if (argc >= 2) {
	strncpy(dev_info.serial, argv[1], sizeof(dev_info.serial) - 1);
	}
	// Open the device
	status = bladerf_open_with_devinfo(&dev, &dev_info);
	if (status != 0) {
	 fprintf(stderr, "Unable to open device: %s\n",
	 bladerf_strerror(status));
	 return 1;
	}
	
	// Start transmission config
	setup:
	// TxConfig is the struct with all config values
	
	get_config(&txc);
	/* Set up TX channel parameters */
	config.channel = BLADERF_CHANNEL_TX(txc.channel-1);
	config.frequency = txc.freq;
	config.bandwidth = txc.bandwidth;
	config.samplerate = SAMPLE_RATE;
	config.gain = 0;
	status = configure_channel(dev, &config);
	if (status != 0) {
		fprintf(stderr, "Failed to configure TX channel. Exiting.\n");
		goto out;
	}
	printf("Tx Freq %d\n", config.frequency);
	printf("Tx Band %d\n", config.bandwidth);
	 
	/* 
	* Populate signal buffer for given amplitude/duration
	*/
	int16_t *tx_samples  = NULL;
	tx_samples = malloc(txc.num_samples * 2 * 1 * sizeof(int16_t));
	if (tx_samples == NULL) {
		perror("malloc");
		free(tx_samples);
		return BLADERF_ERR_MEM;
	}	
	produce_samples(txc.pwr, tx_samples, txc.num_samples);
	
	const unsigned int num_buffers = 16;
	const unsigned int buffer_size = 20480; /* Must be a multiple of 1024 */
	const unsigned int num_transfers = 8;
	const unsigned int timeout_ms = 3500;
	/* Configure both the device's x1 RX and TX channels for use with the
	* synchronous
	* interface. SC16 Q11 samples *without* metadata are used. */
	status = bladerf_sync_config(dev, BLADERF_TX_X1, BLADERF_FORMAT_SC16_Q11,
	num_buffers, buffer_size, num_transfers, timeout_ms);
	if (status != 0) {
		fprintf(stderr, "Failed to configure TX sync interface: %s\n",
		bladerf_strerror(status));
	}
	status = bladerf_enable_module(dev, BLADERF_TX, true);
	if (status != 0) {
		fprintf(stderr, "Failed to enable TX: %s\n", bladerf_strerror(status));
		goto out;
	}
	
	while(txc.tx){
		printf("TX Running\n");
		// Make call to start tx; either sync or mimo;
		status = bladerf_sync_tx(dev, tx_samples, txc.num_samples, NULL, 5000);
		// Error Check
		if (status != 0) {
			fprintf(stderr, "Failed to TX samples: %s\n", bladerf_strerror(status));
			goto out;
		 }
		 if (status == 0) {
			/* Wait a few seconds for any remaining TX samples to finish
			* reaching the RF front-end */
			usleep(2000000);
			goto out;
		}

	}
	// Turn off module
	status = bladerf_enable_module(dev, BLADERF_TX, false);
	if (status != 0) {
	fprintf(stderr, "Failed to disable TX: %s\n", bladerf_strerror(status));
	}
	//
 
	out:
	// close device connection and free any used memory;
	free(tx_samples);	
	bladerf_close(dev);
	return status;
}


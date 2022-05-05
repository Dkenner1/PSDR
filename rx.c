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
	RxConfig rxc;
	
	// Initilize the device
	bladerf_init_devinfo(&dev_info);
	// Request a device with the provided serial number.
	// Invalid strings should simply fail to match a device. 
	
	setup:
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
    /* Set up RX channel parameters */
    config.channel    = BLADERF_CHANNEL_RX(0);
    config.frequency  = 910000000;
    config.bandwidth  = 2000000;
    config.samplerate = 300000;
    config.gain       = 39;


	// Set configuration values
    status = configure_channel(dev, &config);
    if (status != 0) {
        fprintf(stderr, "Failed to configure RX channel. Exiting.\n");
        goto out;
    }
 


	int16_t *tx_samples  = NULL;
	rx_samples = malloc(rxc.num_samples * 2 * 1 * sizeof(int16_t));
	if (tx_samples == NULL) {
		perror("malloc");
		free(tx_samples);
		return BLADERF_ERR_MEM;
	}	

	
	const unsigned int num_buffers = 64;
	const unsigned int buffer_size = 40960; // Must be a multiple of 1024
	const unsigned int num_transfers = 8;
	const unsigned int timeout_ms = 3500;

	
	status = bladerf_enable_module(dev, BLADERF_CHANNEL_TX(rxc.channel-1), true);
	if (status != 0) {
		fprintf(stderr, "Failed to enable TX: %s\n", bladerf_strerror(status));
		goto out;
	}
	while(rxc.tx){
	//Turn module on

		struct timeval stop, start;
		gettimeofday(&start, NULL);
		// Make call to start tx; either sync or mimo;
		// transmit buffer
		
		status = bladerf_sync_tx(dev, tx_samples, rxc.num_samples, NULL, 
			(rxc.num_samples/rxc.sample_rate)*1500); 
		if (status != 0) {
			fprintf(stderr, "Failed to TX samples: %s\n", bladerf_strerror(status));
			goto out;
		 }
		// Wait a few seconds for TX samples to finish reaching the RF front-end 
		usleep(rxc.num_samples*.90);

		if(rxc.t_mode==PULSE){
			status = bladerf_enable_module(dev, BLADERF_CHANNEL_TX(rxc.channel-1), false);
			if (status != 0) 
				fprintf(stderr, "Failed to disable TX: %s\n", bladerf_strerror(status));
			usleep(pulse_delay*.97);
			if(rxc.c_mode==SINGLE){
				status = bladerf_sync_config(dev, BLADERF_TX_X1, BLADERF_FORMAT_SC16_Q11,
				num_buffers, buffer_size, num_transfers, timeout_ms);
			}
			else{
				status = bladerf_sync_config(dev, BLADERF_TX_X2, BLADERF_FORMAT_SC16_Q11,
				num_buffers, buffer_size, num_transfers, timeout_ms);
			}
			if (status != 0) {
				fprintf(stderr, "Failed to configure TX sync interface: %s\n",
				bladerf_strerror(status));
			}
			status = bladerf_enable_module(dev, BLADERF_CHANNEL_TX(rxc.channel-1), true);
		}
		
		print_rxConfig(&rxc);
		gettimeofday(&stop, NULL);
		printf("Transmit took %lu us\n", (stop.tv_sec - start.tv_sec) * 1000000 + stop.tv_usec - start.tv_usec);
		if(config_changed(&rxc)){
			printf("Config Changed!\n");
			status = bladerf_enable_module(dev, BLADERF_CHANNEL_TX(rxc.channel-1), false);
			if (status != 0) {
				fprintf(stderr, "Failed to disable TX: %s\n", bladerf_strerror(status));
			}
			bladerf_close(dev);
			goto setup;
		}
	}
	
 	printf("Exiting\n");
	out:
	// Turn off module
	status = bladerf_enable_module(dev, BLADERF_CHANNEL_TX(rxc.channel-1), false);
	if (status != 0) {
	fprintf(stderr, "Failed to disable TX: %s\n", bladerf_strerror(status));
	}
	
	// close device connection and free any used memory;
	free(tx_samples);	
	bladerf_close(dev);
	
	return 0;//status;
	
}

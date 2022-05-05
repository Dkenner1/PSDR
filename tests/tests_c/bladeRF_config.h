// Compile with: $ gcc -o bin/bladeRF_config.o -c test/bladeRF_config.c

#ifndef _BLADERF_CONFIG_H_
#define _BLADERF_CONFIG_H_
#define CONFIG_SIZE 12
#include <stdint.h>

static const uint8_t SINGLE=0, CONTINUOUS=0, OFF=0, COUPLED=0;
static const uint8_t MIMO=1, PULSE=1, ON=1, DECOUPLED=1;

static const int GAIN_MAX=66;
static const int GAIN_MIN=-23;

typedef struct {
	int gain;
	unsigned int freq;
	unsigned int bandwidth;
	unsigned int num_samples;
	unsigned int sample_rate;
	float pwr;
	float duty_cycle;
	uint8_t tx;
	uint8_t channel;
	uint8_t t_mode;
	uint8_t c_mode;
	uint8_t g_mode;
	
} TxConfig;

typedef struct {
    char *key;
    char *value;
}  keyValue;


int get_config(TxConfig *config);
int format_entry(char *str, char *fstr);
char * get_keyValue(char *str, keyValue *list);
int get_keyIndex(char *str, keyValue *list);
int config_changed(TxConfig *config);
void print_TxConfig(TxConfig *config);

#endif

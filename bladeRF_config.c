#include <libbladeRF.h>
#include "bladeRF_config.h"
#include <string.h>
#include <stdlib.h>
#include <stdio.h>

void print_TxConfig(TxConfig *config){
	printf("Freq: %d\n", config->freq);
	printf("Bandwidth: %d\n", config->bandwidth);
	printf("num_samples: %d\n", config->num_samples);
	printf("pwr: %f\n", config->pwr);
	printf("duty_cycle: %f\n", config->duty_cycle);
	printf("channel: %d\n", config->channel);
	printf("t_mode: %d\n", config->t_mode);
	printf("c_mode: %d\n", config->c_mode);
	printf("g_mode: %d\n", config->g_mode);
	printf("gain: %d\n", config->gain);
	printf("Sample Rate: %d\n", config->sample_rate);
}

void print_TxConfig(RxConfig *config){
	printf("Frequency: %d\n", config->freq);
	printf("Number Samples: %d\n", config->num_samples);
	printf("Sample Rate: %d\n", config->sample_rate);
	printf("Channel: %d\n", config->channel);
	printf("Gain: %d\n", config->gain);
}


int config_changed(TxConfig *config){
	TxConfig *temp = malloc(sizeof(TxConfig));
	memcpy((void *) temp, (void *)  config, sizeof(TxConfig));
	memset(config, 0, sizeof(config));
	get_config(config);	
	if(temp->freq != config->freq ||
		temp->bandwidth != config->bandwidth ||
		temp->num_samples != config->num_samples ||
		temp->pwr != config->pwr ||
		temp->duty_cycle != config->duty_cycle ||
		temp->channel != config->channel ||
		temp->t_mode != config->t_mode ||
		temp->c_mode != config->c_mode ||
		temp->g_mode != config->g_mode ||
		temp->gain != config->gain ||
		temp->sample_rate != config->sample_rate)
	{
		memset(temp, 0, sizeof(TxConfig));
		return 1;
	}
	memset(temp, 0, sizeof(TxConfig));
	return 0;
}

int rx_config_changed(RxConfig *config){
	RxConfig *temp = malloc(sizeof(RxConfig));
	memcpy((void *) temp, (void *)  config, sizeof(RxConfig));
	memset(config, 0, sizeof(config));
	get_config(config);
	if(temp->freq != config->freq ||
		temp->bandwidth != config->bandwidth ||
		temp->num_samples != config->num_samples ||
		temp->bw_mode != config->bw_mode ||
		temp->gain != config->gain ||
		temp->sample_rate != config->sample_rate)
	{
		memset(temp, 0, sizeof(RxConfig));
		return 1;
	}
	memset(temp, 0, sizeof(RxConfig));
	return 0;
}


int get_config(TxConfig *config){
	static const int MAX_LINE_SIZE = 255;
	static const int MAX_KEYS=64;
	static const int MAX_KEYVALUE_LEN;
    FILE *fp = fopen("etc/bladeRF_TxConfig.ini", "r+");
    if(fp==NULL)
    	return -1;
    	
    keyValue *keys = malloc(0);
    char line[MAX_LINE_SIZE];
    char (*formatted)[40] = malloc(MAX_KEYS * sizeof(*formatted));
    
    int i=0;
    while(fgets(line, MAX_LINE_SIZE+1, fp)){
    	if(line[0]=='#' || line[0]=='\n'){
    		memset(line, 0, MAX_LINE_SIZE);
    		continue;
    	}
    	if(i >= MAX_KEYS)
    		return -1;
    		
    	keys=realloc(keys, (i + 1) * sizeof(keyValue));
    	format_entry(line, formatted[i]);
    	//split into key value pairs
    	keys[i].key = strtok(formatted[i], "=");
		keys[i].value = strtok(NULL, "=");
		i++;
		memset(line, 0, MAX_LINE_SIZE);
    }
    
    config->freq=atoi(get_keyValue("freq", keys));
    config->bandwidth=atoi(get_keyValue("bandwidth", keys));
    config->num_samples=atoi(get_keyValue("num_samples", keys) );
    config->sample_rate=atoi(get_keyValue("sample_rate", keys));
    config->gain=atoi(get_keyValue("gain", keys));
    
    config->pwr=atof(get_keyValue("pwr", keys));  
    config->duty_cycle=atof(get_keyValue("duty_cycle", keys));
    
	
    if(!strcmp(get_keyValue("channel_mode", keys), "mimo"))
    	config->c_mode=MIMO;
	else
    	config->c_mode=SINGLE; 
	
    if(!strcmp(get_keyValue("tx_mode", keys), "pulse"))
    	config->t_mode=PULSE;
    else
    	config->t_mode=CONTINUOUS;
 
     if(!strcmp(get_keyValue("gain_mode", keys), "coupled"))
    	config->g_mode=COUPLED;
    else
    	config->g_mode=DECOUPLED;
    	
    if(atoi(get_keyValue("tx", keys))==ON)
    	config->tx=ON;
    else
    	config->tx=OFF; 

    if(atoi(get_keyValue("channel", keys)) == 2)
    	config->channel=2;
    else
    	config->channel=1; 

	memset(keys, 0, sizeof(keyValue)*i);
    free(keys);
    free(formatted);
    fclose(fp);
	return 0;
};

int get_rx_config(RxConfig *config){
	static const int MAX_LINE_SIZE = 255;
	static const int MAX_KEYS=64;
	static const int MAX_KEYVALUE_LEN;
    FILE *fp = fopen("etc/bladeRF_TxConfig.ini", "r+");
    if(fp==NULL)
    	return -1;
    keyValue *keys = malloc(0);
    char line[MAX_LINE_SIZE];
    char (*formatted)[40] = malloc(MAX_KEYS * sizeof(*formatted));

    int i=0;
    while(fgets(line, MAX_LINE_SIZE+1, fp)){
    	if(line[0]=='#' || line[0]=='\n'){
    		memset(line, 0, MAX_LINE_SIZE);
    		continue;
    	}
    	if(i >= MAX_KEYS)
    		return -1;

    	keys=realloc(keys, (i + 1) * sizeof(keyValue));
    	format_entry(line, formatted[i]);
    	//split into key value pairs
    	keys[i].key = strtok(formatted[i], "=");
		keys[i].value = strtok(NULL, "=");
		i++;
		memset(line, 0, MAX_LINE_SIZE);
    }

    config->freq=atoi(get_keyValue("rx_freq", keys));
    config->bandwidth=atoi(get_keyValue("rx_bandwidth", keys));
    config->num_samples=atoi(get_keyValue("rx_num_samples", keys) );
    config->sample_rate=atoi(get_keyValue("rx_sample_rate", keys));
    config->gain=atoi(get_keyValue("rx_gain", keys));

    if(atoi(get_keyValue("rx", keys))==ON)
    	config->rx=ON;
    else
    	config->rx=OFF;

    if(atoi(get_keyValue("channel", keys)) == 2)
    	config->channel=2;
    else
    	config->channel=1;

	memset(keys, 0, sizeof(keyValue)*i);
    free(keys);
    free(formatted);
    fclose(fp);
	return 0;
};

// Return value of keyValue
// Hashtable would be more elegant solution
// Does not return index to prevent segmentation fault issues
// from failing to check if the key exists.
char* get_keyValue(char *str, keyValue *list){
    int index = get_keyIndex(str, list);;
    return index != -1 ? list[index].value : "\n";
};

int get_keyIndex(char *str, keyValue *list){
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
	while(*str !='\n'){
	char c=*str++;
	if(c==' ')
		continue;
	if(c>='A' && c<='Z')
		c+=32; 
	*fstr=c;
	*fstr++;	
	}
	*fstr='\0';
}



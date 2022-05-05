function set_freq(freq, varargin)
    if(size(varargin) > 1)
        error("Too many input arguments")
    end    
    if(isempty(varargin))
       config_path = bladeRF.config_path;
    else
        config_path=varargin{1};
    end
    if(freq >= 47000000 && freq <= 6000000000)
        update_config("freq", freq, config_path)
    else
       error("Input value not in valid range: 47000000 - 6000000000");
    end
end
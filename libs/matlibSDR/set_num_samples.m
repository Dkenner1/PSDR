function set_num_samples(nsamples, varargin)
    if(size(varargin) > 1)
        error("Too many input arguments")
    end    
    if(isempty(varargin))
       config_path = bladeRF.config_path;
    else
        config_path=varargin{1};
    end
    if(nsamples >= 521000 && nsamples <= 61440000)
        update_config("num_samples", nsamples, config_path)
    else
       error("Input value not in valid range: 521000 - 61440000");
    end
end


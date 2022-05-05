function set_bandwidth(bw, varargin)
    if(size(varargin) > 1)
        error("Too many input arguments")
    end    
    if(isempty(varargin))
       config_path = bladeRF.config_path;
    else
        config_path=varargin{1};
    end
    if(bw >= 200000 && bw <= 56000000)
        update_config("bandwidth", bw, config_path)
    else
       error("Supplied value not in valid range: 200000 - 56000000");
    end
end

function set_pwr(pwr, varargin)
    if(size(varargin) > 1)
        error("Too many input arguments")
    end    
    if(isempty(varargin))
       config_path = bladeRF.config_path;
    else
        config_path=varargin{1};
    end
    if(pwr >= 0 && pwr <= 100)
        update_config("pwr", pwr, config_path)
    else
       error("Invalid input, Value must be in range: [0, 100]")
    end
end


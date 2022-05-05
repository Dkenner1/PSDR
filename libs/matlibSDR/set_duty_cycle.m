function set_duty_cycle(duty_cycle, varargin)
    if(size(varargin) > 1)
        error("Too many input arguments")
    end    
    if(isempty(varargin))
       config_path = bladeRF.config_path;
    else
        config_path=varargin{1};
    end
    if(duty_cycle >= 0 && duty_cycle <= 100)
        update_config("duty_cycle", duty_cycle, config_path)
    else
       error("Invalid input, Value must be in range: [0, 100]");
    end
end


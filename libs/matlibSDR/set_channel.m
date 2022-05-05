function set_channel(ch, varargin)
    if(size(varargin) > 1)
        error("Too many input arguments")
    end    
    if(isempty(varargin))
       config_path = bladeRF.config_path;
    else
        config_path=varargin{1};
    end
    if(ch == 1 || ch == 2)
        update_config("channel", ch, config_path)
    else
       error("Undefined Channel: Acceptable values: 1, 2");
    end
end


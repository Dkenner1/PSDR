function enable_bladeRF(varargin)
    if(size(varargin) > 1)
        error("Too many input arguments")
    end    
    if(isempty(varargin))
       config_path = bladeRF.config_path;
    else
        config_path=varargin{1};
    end
    update_config("tx", 1, config_path)
end


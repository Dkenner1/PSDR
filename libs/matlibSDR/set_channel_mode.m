function set_channel_mode(ch, varargin)
    if(size(varargin) > 1)
        error("Too many input arguments")
    end    
    if(isempty(varargin))
       config_path = bladeRF.config_path;
    else
        config_path=varargin{1};
    end
    if(ch == bladeRF.CMode_SINGLE || ch == bladeRF.CMode_MIMO)
        update_config("channel_mode", ch, config_path)
    else
       error("Invalid Channel Mode, use bladeRF constants class.\n Valid channel modes: 'single', 'mimo'");
    end
end


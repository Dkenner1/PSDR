function set_tx_mode(ch, varargin)
    if(size(varargin) > 1)
        error("Too many input arguments")
    end    
    if(isempty(varargin))
       config_path = bladeRF.config_path;
    else
        config_path=varargin{1};
    end
    if(ch == bladeRF.TxMode_CONTINUOUS || ch == bladeRF.TxMode_PULSE)
        update_config("tx_mode", ch, config_path)
    else
       error("Invalid Tx Mode, use bladeRF constants class.\n Valid channel modes: 'continuous', 'pulse'");
    end
end


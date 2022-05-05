function value = get_config_value(key, config_path)
    fid = fopen(config_path, "r");
    while ~feof(fid)
        line = fgetl(fid);
    end
    fclose(fid);
end


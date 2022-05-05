function update_config(key, newValue, config_path)
    config = load_file(config_path);
    % Find key, if no key present skip
    for i = 1:size(config, 2)
        line=config{i};
        if (isempty(line) || line(1) == "#")
            continue
        end
        line=strrep(line,' ', '');
        keyValue = split(line, "=");
        if(keyValue{1}==key)
            config{i} = join([keyValue{1}, string(newValue)], "=");
            break;
        end
    end
    
    fileID = fopen(config_path,'w');
    for i=1:size(config, 2)
        fprintf(fileID, '%s\n',config{i});
    end
    fclose(fileID);
end


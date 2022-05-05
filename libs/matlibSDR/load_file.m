function textArr = load_file(config_path)
%LOAD_FILE 
%
%
%   
    fid = fopen(config_path, "r");
    textArr = {};
    while ~feof(fid)
        textArr{end+1} = fgetl(fid);
    end
    fclose(fid);
end


function printFile(config_path)
    fid = fopen(config_path, "r");
    while ~feof(fid)
        disp(fgetl(fid));
    end
    fclose(fid);
end



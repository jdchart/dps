// TODO: some of these should be other things than posts...

export const is_file = async (path) => {
    /* Check if given file exists. */
    const response = await fetch('', {
        method: 'POST',
        body: JSON.stringify({
            type : "doesFileExist",
            path : path
        }),
        headers: {
            'content-type': 'application/json'
        }
    });
    let rep = await response.json();
    return rep;
};

export const createDir = async (path) => {
    /*
    Create a new dir (in src or static)
    */
    const response = await fetch('', {
        method: 'POST',
        body: JSON.stringify({
            type : "createDir",
            dirPath : path
        }),
        headers: {
            'content-type': 'application/json'
        }
    });
    await response.json();
};

export const writeFile = async (path, content) => {
    /*
    Write a file to any path (in src or static)
    */
    const response = await fetch('', {
        method: 'POST',
        body: JSON.stringify({
            codeContent : content,
            type : "writeFile",
            fileName : path
        }),
        headers: {
            'content-type': 'application/json'
        }
    });
    await response.json();
};

export const read_json = async (path) => {
    /* Read a file to any path (in src or static). */
    const response = await fetch('', {
        method: 'POST',
        body: JSON.stringify({
            type : "readFile",
            fileName : path
        }),
        headers: {
            'content-type': 'application/json'
        }
    });
    let rep = await response.json();
    return rep["content"]
};

export const getDirTree = async (path, recusive = true, accepted = []) => {
    /*
    Return the folder hierarchy
    */
    const response = await fetch('', {
        method: 'POST',
        body: JSON.stringify({
            type : "getTree",
            path : path,
            recursive : recusive,
            accepted : accepted
        }),
        headers: {
            'content-type': 'application/json'
        }
    });
    let rep = await response.json();
    return rep;
};

export const get_dirs = async (path, recursive = true) => {
    /*
    Return the folders in a dir
    */
    const response = await fetch('', {
        method: 'POST',
        body: JSON.stringify({
            type : "getDirs",
            path : path,
            recursive : recursive
        }),
        headers: {
            'content-type': 'application/json'
        }
    });
    let rep = await response.json();
    return rep;
};

export const getFiles = async (path, recursive = true, accepted = []) => {
    /*
    Return the files in a dir
    */
    const response = await fetch('', {
        method: 'POST',
        body: JSON.stringify({
            type : "getFiles",
            path : path,
            recursive : recursive,
            accepted : accepted
        }),
        headers: {
            'content-type': 'application/json'
        }
    });
    let rep = await response.json();
    return rep;
};
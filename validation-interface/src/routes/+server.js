import { json } from '@sveltejs/kit';

import { writeFile, existsSync, readdirSync, statSync, readFileSync, mkdirSync } from 'fs';
import { extname } from "path";


export async function POST({ request }) {
  const myData = await request.json();

  if(myData.type === "writeFile"){
    await writeAsync(myData.fileName, myData.codeContent)
    return json(myData);
  };

  if(myData.type === "doesFileExist"){
    let rep;
    rep = await existsSync(myData.path);
    return json(rep);
  };

  if(myData.type === "getDirs"){
    let rep = getDirs(myData.path, myData.recursive);
    return json(rep)
  };

  if(myData.type === "getTree"){
    let rep = getDirTree(myData.path, myData.recursive, myData.accepted);
    return json(rep)
  };

  if(myData.type === "getFiles"){
    let rep = getFiles(myData.path, myData.recursive, myData.accepted);
    return json(rep)
  };

  if(myData.type === "readFile"){
    let rep = readJsonFile(myData.fileName);
    return json(rep)
  };

  if(myData.type === "createDir"){
    mkdirSync(myData.dirPath);
    return json(myData);
  };
};

function readJsonFile(path){
  let content = {};
  
  // readFile(path, 'utf8', function(err, data){ 
  //   content = JSON.parse(data); 
  // });

  content = JSON.parse(readFileSync(path, 'utf8'))
  return {"content" : content}
}

async function writeAsync(path, data){
  /*
  Create a new file with the given data at the given path.
  */
  await writeFile(path, data, () => {
    //console.log("callback");
  })
};

function getDirs(path, recursive = true){
  /*
  Return a list of folders at the given path.
  (can set recursive)
  */
  let ret = [];
  readdirSync(path, { withFileTypes: true }).forEach(function(item){
    if(item.isDirectory()){
      ret.push({
        "name" : item.name,
        "path" : path + '/' + item.name
      });
      if(recursive){
        ret = ret.concat(getDirs(path + '/' + item.name, recursive))
      }
    }
  });
  return ret
};

function getFiles(path, recursive = true, accepted = []){
  /*
  Return a list of files at the given path.
  (can set recursive)
  */
  let ret = [];
  readdirSync(path, { withFileTypes: true }).forEach(function(item){
    if(item.isFile()){
      const stats = statSync(path + '/' + item.name);
      const creationTime = stats.birthtime;
      ret.push({
        "name" : item.name,
        "path" : path + '/' + item.name,
        "creation" : creationTime
      });
    }
    else if(item.isDirectory()){
      if(recursive){
        ret = ret.concat(getFiles(path + '/' + item.name, recursive))
      }
    };
  });
  return ret
};

function getDirTree(dirPath, recursive = true, accepted = []){
  /*
  Return a list of files at the given path
  (can set recusrive and a list of accpeted .extensions).
  */
  var results = [];
  readdirSync(dirPath).forEach(function(file) {
    file = dirPath+'/'+file;
    var stat = statSync(file);
    if (stat && stat.isDirectory() && recursive) {
        results = results.concat(getDirTree(file, recursive, accepted))
    } else{
      if (accepted.length === 0){
        results.push(file);
      }
      else if(accepted.includes(extname(file))){
        results.push(file);
      }
    } 
  });
  return results
};
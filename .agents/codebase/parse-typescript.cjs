const fs = require('node:fs');
const cp = require('node:child_process');
const path = require('node:path');
let ts;
try { ts = require('typescript'); } catch {
  try { ts = require(path.join(cp.execFileSync('npm',['root','-g'],{encoding:'utf8',timeout:5000}).trim(),'typescript')); }
  catch { console.error('Thiếu TypeScript Compiler API'); process.exit(2); }
}
const input=JSON.parse(fs.readFileSync(0,'utf8'));
const output=input.map(({path:filename,text})=>{
 const source=ts.createSourceFile(filename,text,ts.ScriptTarget.Latest,true);
 const symbols=[],imports=[],calls=[];
 const where=n=>({line:source.getLineAndCharacterOfPosition(n.getStart(source)).line+1,end_line:source.getLineAndCharacterOfPosition(n.getEnd()).line+1});
 function record(n,name,kind,prefix){
   const entry={name:prefix+name,kind,...where(n)};
   if(n.parameters)entry.parameters=n.parameters.map(p=>({name:p.name.getText(source),type:p.type?.getText(source)||null,optional:!!p.questionToken||!!p.initializer,rest:!!p.dotDotDotToken}));
   if(n.type)entry.return_type=n.type.getText(source);
   symbols.push(entry);return prefix+name+'.';
 }
 function walk(n,prefix=''){
   let sub=prefix;
   if(ts.isImportDeclaration(n)||ts.isExportDeclaration(n)){if(n.moduleSpecifier&&ts.isStringLiteral(n.moduleSpecifier))imports.push({path:n.moduleSpecifier.text,...where(n)});}
   if(ts.isCallExpression(n)||ts.isNewExpression(n)){
      calls.push({name:n.expression.getText(source),...where(n)});
      if(n.arguments?.length&&ts.isStringLiteral(n.arguments[0])&&(n.expression.kind===ts.SyntaxKind.ImportKeyword||n.expression.getText(source)==='require'))imports.push({path:n.arguments[0].text,...where(n)});
   }
   if(ts.isClassDeclaration(n)||ts.isClassExpression(n)||ts.isInterfaceDeclaration(n)||ts.isEnumDeclaration(n)||ts.isTypeAliasDeclaration(n)||ts.isFunctionDeclaration(n)||ts.isMethodDeclaration(n)||ts.isMethodSignature(n)||ts.isConstructorDeclaration(n)||ts.isGetAccessorDeclaration(n)||ts.isSetAccessorDeclaration(n)){
      const name=n.name?.getText(source)||(ts.isConstructorDeclaration(n)?'constructor':`ẩn_danh_${where(n).line}`);
      sub=record(n,name,ts.SyntaxKind[n.kind],prefix);
   }else if((ts.isVariableDeclaration(n)||ts.isPropertyDeclaration(n)||ts.isPropertyAssignment(n))&&n.initializer&&(ts.isArrowFunction(n.initializer)||ts.isFunctionExpression(n.initializer))){
      sub=record(n.initializer,n.name.getText(source),ts.SyntaxKind[n.initializer.kind],prefix);
   }else if(ts.isVariableDeclaration(n)||ts.isPropertyDeclaration(n)||ts.isPropertySignature(n)){
      sub=record(n,n.name.getText(source),ts.SyntaxKind[n.kind],prefix);
   }
   ts.forEachChild(n,c=>walk(c,sub));
 }
 walk(source);
 return {path:filename,status:source.parseDiagnostics.length?'PARSE_BLOCKED':'STATIC_AST',symbols,imports,calls,diagnostics:source.parseDiagnostics.map(d=>ts.flattenDiagnosticMessageText(d.messageText,' '))};
});
process.stdout.write(JSON.stringify(output));

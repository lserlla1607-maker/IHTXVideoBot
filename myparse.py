def TemplateParse(content:str,args:str):
  argslen = args.count(" ")
  out = content.replace("{args}",args)
  out = out.replace("{argslen}",str(argslen))
  return our
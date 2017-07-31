#!/usr/bin/python
# -*- coding:utf-8 -*-

out = open("sources.tsv", "w")

f_name = "sources.reverb"
sources = {}
with open(f_name, "r") as df:
	for ligne in df.readlines():
		spl = ligne.strip().split("\t")
		if len(spl) == 2:
			spl_sources = spl[1].split("|")
			out.write(spl[0]+"\t"+str(len(spl_sources))+"\n")																				

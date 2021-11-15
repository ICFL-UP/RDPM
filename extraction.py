import os
import json
from collections import Counter
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
 

features = pd.DataFrame(None, columns = ['r', 'rw', 'rx', 'rwc', 'rwx', 'rwxc', 'label', 'category','sample'])
weight = {'r': 0.1, 'rw': 0.2, 'rx': 0.4, 'rwc': 0.3, 'rwx': 0.5, 'rwxc': 0.6}
failed = []

def walk(folder):
	global failed
	for root, dirs, files in os.walk(folder, topdown=False):
		for name in files:
			try:
				# if not os.path.exists(name.split(".")[0]):
				# 	os.makedirs(name.split(".")[0])
				print(os.path.join(root, name))
				data = json.load(open(os.path.join(root, name), 'r'))
				print(data.keys())
				sequence = ""
				rleSeq = ""
				count = 0
				if "procmemory" in data.keys():
					for procMem in data["procmemory"]:
						count += 1
						seq = ""
						crle = 1
						prev = ""
						rle = ""
						graph_data = {'r': [], 'rw': [], 'rx': [], 'rwc': [], 'rwx': [], 'rwxc': []}
						for regions in procMem["regions"]:					
							seq += regions["protect"] + " "
							if prev == "":
								prev = regions["protect"]
							elif prev == regions["protect"]:
								crle += 1
							else:
								graph_data[prev].append(crle)
								rle += str(crle) + prev
								crle = 1
								prev = regions["protect"]

						print("\n--------------------------------\nMemory Region: " + str(count))
						count_occurances(procMem["regions"], name)
						print("Sequence ("+ str(count) +"): " + seq)
						print("RLE (" + str(count) + "): " + rle)

						x = []
						y = []
						l = []
						# for k, v in graph_data.items():
						# 	# plt.figure(count)
						# 	plt.plot(np.arange(0, len(v)), v, label=k)
						# 	plt.legend()
						# 	plt.suptitle(name + " - " + str(count) + " " + k)
						# 	plt.savefig(name.split(".")[0]+"/"+name + "_" + str(count)+ k +".png")
						# 	plt.close()
						# 	plt.clf()

							# x.append(list(np.arange(0, len(v))))
							# y.append(v)  #[x * weight[k] for x in v]
							# l.append(k)
							# plt.figure(0)
							# plt.plot(, , label=k)
							# plt.figure(count)					
							

						# plt.clf()
						# plt.close('all') 
						# plt.plot(x,y,label=l[0])
						# plt.legend()
						# plt.suptitle(name + " - " + str(count) + " - All" )
						# plt.savefig(name.split(".")[0]+"/"+name + "_" + str(count) + ".png")
						# plt.clf()
						# plt.close('all')
						print("Data ("+ str(count) +"): " + str(graph_data))

						sequence += seq
						rleSeq += rle
				else:
					failed.append(os.path.join(root, name))
			except:
				print("FAILED AT: " + name)
				continue

		print("\n\nOverall Sequence: " + sequence)
		print("\nOverall RLE: " + rleSeq)
		print("\nCount: " + str(count))



def count_occurances(d, n):
	signs = Counter(k['protect'] for k in d if k.get('protect'))
	feat = {'r': 0, 'rw': 0, 'rx': 0, 'rwc': 0, 'rwx': 0, 'rwxc': 0, 'label': n[0], 'category': n.split("_")[1], 'sample': n}
	global features
	for sign, count in signs.most_common():
		feat[sign] = count
	features = features.append(feat, ignore_index=True)
 

# ------ Script
walk("..\\Reports")
print(features)
plot = features.plot()
fig = plot.get_figure()
fig.savefig("ALL_FEATURES.png")
plt.close('all')
features.to_excel("features.xlsx")
print("FAILED: " + str(failed))

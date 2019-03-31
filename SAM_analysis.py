def read_sam(filename):
	with open(filename, 'r') as f: # open sam file
		lines = f.readlines()
		mapping_quality_threshold = 13 # set mapping quality
		pairs = {} # dictionary to store all pairs
		for line in lines:
			try: 
				temp = line.split('\t')
				sum_flag = int(temp[1]) # get the flag value
				alignment = break_flag(sum_flag) # split up the flag value into its respective bits 
				mapping_quality = int(temp[4]) 
				if (alignment[2] == 0 and alignment[3] == 0) and mapping_quality > mapping_quality_threshold: # mapped alignments exists
					ref = temp[2]
					ref_pos = temp[3]
					ref_mate = temp[6]
					ref_mate_pos = temp[7]
					if ref_mate != '=' and (ref_mate == 'TY5' or ref == 'TY5'): # map to chromosome and transposon
						if alignment[6] == 1: # if it is mate 1
							pair = ref+'-'+ref_pos+' --- '+ref_mate+'-'+ref_mate_pos
						else:
							pair = ref_mate+'-'+ref_mate_pos+' --- '+ref+'-'+ref_pos
						if pair not in pairs:
							pairs[pair] = []
						pairs[pair].append(temp[2:8]) # [RNAME, POS, MAPQ, CIGAR, RNEXT, PNEXT]
			except:
				continue
		find_pairs(pairs)

def break_flag(sum_flag): # split up the flag value into its respective bits
	flags = [1,2,4,8,16,32,64,128]
	output = [0,0,0,0,0,0,0,0]
	flag_index = 7
	while sum_flag > 0:
		curr_flag = flags[flag_index]
		if sum_flag >= curr_flag:
			sum_flag -= curr_flag
			output[flag_index] = 1
		flag_index -= 1
	return output

def find_pairs(pairs):
	for pair in pairs:
		if len(pairs[pair]) > 1: # both ends have MAPQ higher than threshold
			print(pairs[pair])

read_sam('A0171771A_R.sam')
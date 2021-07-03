from src.midiutil.MidiFile3 import MIDIFile
import random
import argparse

MyMIDI = MIDIFile(2)

"""
	INSTRUMENT CLASS
"""
class Instrument:
	def __init__(self, instrument_name, instrument_number, track, channel):
		self.instrument_name = instrument_name
		self.instrument_number = instrument_number
		self.track = track
		self.channel = channel
		self.volume = 100
		self.duration = random.uniform(0.25, 1)


"""
	MELODY NOTES
"""
MELODY_SCALES = [
	[60, 62, 64, 67, 69],  # pentatonic scale - C, D, E, G, A
	[60, 63, 65, 66, 67, 70, 72] #c_blue - C, Eb, F, Gb, G, Bb, C
]

"""
	INSTRUMENT GM NUMBERS
"""
PERC_DICT = {
	'drums': (115, 116, 117, 118, 119),
	'elec_bass': (33, 34, 35, 36, 37, 38, 39, 40),
	# 'bass_synth_pad': (89, 90, 91, 92, 93, 94, 95, 96),
	'synth_effects': (97, 98, 99, 100, 101, 102, 103, 104),
	'sound_effects': (120, 121, 122, 127)
}

MEL_DICT = {
	'piano': (1, 2, 3, 4, 5, 6, 7, 8),
	'guitar': (25, 26, 27, 28, 29, 30, 31, 32),
	'mel_synth_pad': (89, 90, 91, 92, 93, 94, 95, 96),
	'ethnic': (105, 106, 107, 108, 109, 110, 111, 112),
	'synth_lead': (81, 82, 83, 84, 85, 86, 87, 88)
}


"""
	CREATE INSTRUMENTS
"""
# instrument_name, instrument_number, track, channel, time, duration
# def create_instrument_objects(number_of_inst, gm_numbers):
# 	inst_object_dict = {}
# 	track = 0
# 	channel = 0
# 	seen_inst = [] #not use duplicate values

# 	choose_perc_inst = random.choice(list(PERC_DICT.values()))
# 	choose_mel_inst = random.choice(list(MEL_DICT.values()))

# 	for _ in range(number_of_inst):
# 		inst_num = random.randint(gm_numbers[0], gm_numbers[1])
# 		if inst_num not in seen_inst:
# 			#instrument_name, instrument_number, track, channel, time, duration
# 			p = Instrument(str(inst_num), inst_num, track, channel)
# 			global MyMIDI
# 			MyMIDI.addTrackName(p.track, 0, p.instrument_name)
# 			MyMIDI.addProgramChange(p.track, p.channel, 0, p.instrument_number)

# 			#percussion_objects_list.append(p)
# 			inst_object_dict[str(track)] = p
# 			track += 1
# 			channel += 1

# 	return inst_object_dict

def create_instrument_objects(number_of_inst, inst_type):
	inst_object_dict = {}
	track = 0
	channel = 0

	if inst_type == 'perc':
		selected_inst = random.sample(list(PERC_DICT.items()), number_of_inst)
	elif inst_type == 'mel':
		selected_inst = random.sample(list(MEL_DICT.items()), number_of_inst)
	else:
		print('Invalid instrument type')

	for counter, si in enumerate(selected_inst):
		if counter < 2 and inst_type == 'perc':
			inst_num = random.choice(PERC_DICT['drums'])
		else:
			inst_num = random.choice(si[1]) #--> get the tuple GM values
		print('inst_class: {}; inst_gm: {}'.format(si[0], inst_num))

		#instrument_name, instrument_number, track, channel, time, duration
		p = Instrument(str(inst_num), inst_num, track, channel)
		global MyMIDI
		MyMIDI.addTrackName(p.track, 0, p.instrument_name)
		MyMIDI.addProgramChange(p.track, p.channel, 0, p.instrument_number)

		#percussion_objects_list.append(p)
		inst_object_dict[str(channel)] = p
		channel += 1

	return inst_object_dict



def produce_output(song_duration, perc_obj_dict, mel_obj_dict):
	#instantiate instruments
	# perc_obj_dict = create_instrument_objects(3, 'perc') #percussion GM ---> 112 - 127
	# mel_obj_dict = create_instrument_objects(1, 'mel') #melody GM ---> 112 - 127

	#keeps track of timing of all instruments playing
	macro_perc_time = 0
	macro_mel_time = 0

	print(perc_obj_dict)
	print(mel_obj_dict)

	p1 = perc_obj_dict['0']
	p2 = perc_obj_dict['1']
	p3 = perc_obj_dict['2']
	# p4 = perc_obj_dict['3']
	m1 = mel_obj_dict['0']


	scale = random.choice(MELODY_SCALES)
	for counter in range(song_duration):

		#percussion line
		MyMIDI.addNote(p1.track, p1.channel, 60, macro_perc_time, p1.duration, p1.volume)
		macro_perc_time += p1.duration
		# print('pl')

		MyMIDI.addNote(p2.track, p2.channel, 60, macro_perc_time, p1.duration, p2.volume)
		macro_perc_time += p2.duration
		# print('p2')

		if counter > 5:
			MyMIDI.addNote(p3.track, p3.channel, 60, macro_perc_time, p1.duration, p3.volume)
			macro_perc_time += p3.duration
			# print('p3')

		# melody time
		mel_duration = random.uniform(0.25, 1)
		MyMIDI.addNote(m1.track, m1.channel, random.choice(scale), macro_mel_time, mel_duration, m1.volume)
		macro_mel_time += mel_duration

	with open('output.mid','wb') as output_file:
		MyMIDI.writeFile(output_file)


def main(song_duration, random_true_or_false, bass_gm_list=None, mel_gm=None):

	#SELECTED INSTRUMENTS
	if random_true_or_false == 'False':
		perc_obj_dict = {}
		mel_obj_dict = {}

		for counter, bg in enumerate(bass_gm_list):
			bass = Instrument(str(bg), bg, 0, counter)
			global MyMIDI
			MyMIDI.addTrackName(bass.track, 0, bass.instrument_name)
			MyMIDI.addProgramChange(bass.track, bass.channel, 0, bass.instrument_number)
			perc_obj_dict[str(counter)] = bass

		mel = Instrument(str(mel_gm), mel_gm, 0, len(bass_gm_list)+1)
		MyMIDI.addTrackName(mel.track, 0, mel.instrument_name)
		MyMIDI.addProgramChange(mel.track, mel.channel, 0, mel.instrument_number)
		mel_obj_dict['0'] = mel 
		produce_output(song_duration, perc_obj_dict, mel_obj_dict)

	#RANDOM INSTRUMENTS
	elif random_true_or_false == 'True':
		#instantiate instruments
		perc_obj_dict = create_instrument_objects(3, 'perc') #percussion GM ---> 112 - 127
		mel_obj_dict = create_instrument_objects(1, 'mel') #melody GM ---> 112 - 127
		produce_output(song_duration, perc_obj_dict, mel_obj_dict)



if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Lit Kpop music produced by a bot')
	parser.add_argument('--length', type=int, default=50)
	parser.add_argument('--random', type=str, default='True')
	args = parser.parse_args()

	if args.random == 'False':
		number_of_perc = input('How many bass instruments (at least 2)? ')
		if int(number_of_perc) >=2:
			bass_gm_list = []
			for i in range(int(number_of_perc)):
				bass_gm = input('Enter GM of bass instrument {}: '.format(i))
				bass_gm_list.append(int(bass_gm))
			mel_gm = int(input('Enter GM of melody instrument: '))
		else:
			print('wtf you did not give 2 instruments. Go back to preschool')

		#bass_gm_list (list)
		#mel_gm (integer)
		main(args.length, args.random, bass_gm_list, mel_gm)

	elif args.random == 'True':
		main(args.length, args.random)

	else:
		print('bruh you didnt properly specify instruments.')

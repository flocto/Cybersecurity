import string
from tqdm import trange
import itertools

# Define the letters
letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

# Define the rotors
class Rotor:
    def __init__(self, wiring, notch=None, ring_setting=0):
        self.wiring = wiring  # Wiring as a string of 26 letters
        self.inverse_wiring = self.calculate_inverse_wiring(wiring)
        self.notch = notch  # Notch position (can be ignored)
        self.position = 0  # Current rotor position (offset)
        self.ring_setting = ring_setting  # Ring setting (0-25)
    
    def calculate_inverse_wiring(self, wiring):
        inverse_wiring = [''] * 26
        for i, ch in enumerate(wiring):
            index = ord(ch) - ord('A')
            inverse_wiring[index] = chr(i + ord('A'))
        return ''.join(inverse_wiring)
    
    def encode_forward(self, ch):
        pos_in = (ord(ch) - ord('A') + self.position - self.ring_setting) % 26
        ch_out = self.wiring[pos_in]
        return ch_out
        # pos_out = (ord(ch_out) - ord('A') - self.position + self.ring_setting) % 26
        # return chr(pos_out + ord('A'))
    
    def encode_backward(self, ch):
        pos_in = (ord(ch) - ord('A') + self.position - self.ring_setting) % 26
        ch_out = self.inverse_wiring[pos_in]
        return ch_out
        # pos_out = (ord(ch_out) - ord('A') - self.position + self.ring_setting) % 26
        # return chr(pos_out + ord('A'))
    
    def step(self):
        self.position = (self.position + 1) % 26
        return self.position == 0

# Define the Enigma machine
class EnigmaMachine:
    def __init__(self, rotors, reflector, rotor_positions=None, plugboard=None):
        self.rotors = rotors  # List of Rotor instances [rotor1, rotor2, rotor3]
        if rotor_positions:
            for rotor, pos in zip(self.rotors, rotor_positions):
                rotor.position = pos
        self.reflector = reflector  # Reflector mapping as a dict
        self.plugboard = plugboard if plugboard else {}  # Plugboard mapping (dict)
    
    def step_rotors(self):
        step_next = self.rotors[0].step()
        if step_next:
            step_next = self.rotors[1].step()
            if step_next:
                self.rotors[2].step()

    def encrypt_character(self, ch):
        if ch not in letters:
            return ch  # Non-letter characters are unchanged
        
        # Apply plugboard
        ch = self.plugboard.get(ch, ch)
        
        # Pass through rotors forward
        for rotor in self.rotors:
            ch = rotor.encode_forward(ch)
        
        # Reflector
        ch = self.reflector.get(ch, ch)
        
        # Pass through rotors backward
        for rotor in reversed(self.rotors):
            ch = rotor.encode_backward(ch)
        
        # Apply plugboard
        ch = self.plugboard.get(ch, ch)
        
        return ch
    
    def encrypt(self, text):
        result = ''
        for ch in text:
            self.step_rotors()
            enc_ch = self.encrypt_character(ch)
            result += enc_ch
        return result

# Define the reflectors
def create_reflector(wiring_str):
    reflector = {}
    for i, ch in enumerate(wiring_str):
        reflector[letters[i]] = ch

    return reflector

reflector = create_reflector('YGQNVUBROLTJZDIWCHXKFEPSAM')
# reflector = create_reflector('CSDLGRTUFWHZXVALNTFMJQBCPY')

# Ciphertext to decrypt
ciphertext = 'KKPEFJZBSVNBYWWOKOJIPNWGPGASCVVYPAYLAHTX'

# Positions to iterate over
positions = range(26)

rotor1 = Rotor('YKNQXBMOVZPIAEJCSDLGRTUFWH')
rotor2 = Rotor('ZXVALNTFMJQBCPYWURSOKDEHIG')
rotor3 = Rotor('RETAIGBSJNUWYXZLPVKCDMQOFH')

for p1, p2, p3 in itertools.product(positions, positions, positions):
    rotor1.position = p1
    rotor2.position = p2
    rotor3.position = p3
    rotors = [rotor1, rotor2, rotor3]
                        
    machine = EnigmaMachine(rotors, reflector)
                        
    # Decrypt the message
    plaintext = machine.encrypt(ciphertext)
    if 'GALF' in plaintext:
        print(plaintext)
        print(f'Positions: {p1} {p2} {p3}')
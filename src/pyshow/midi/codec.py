"""
##########################################
# Simple midi message builder and decode #
##########################################

  Florian Dupeyron
  October 2019

 ----------------------------------------------------------------------------
 "THE BEER-WARE LICENSE" (Revision 42):
 <florian.dupeyron@mugcat.fr> wrote this file. As long as you retain this notice
 you can do whatever you want with this stuff. If we meet some day, and you think
 this stuff is worth it, you can buy me a beer in return !
 ----------------------------------------------------------------------------
"""

from enum import IntEnum,unique

class Midi_Msg:
    """
    Simple midi message representation.

     => SYSTEM MESSAGES NOT HANDLED
     => RPN CC NOT HANDLED
     => CHANNEL MODE MESSAGES NOT HANDLED

     Maybe I will add them one day :o
    """
    @unique
    class Type(IntEnum):
        NOTE_OFF = 0x8,
        NOTE_ON  = 0x9,
        AFTOUCH  = 0xA,
        CC       = 0xB,
        PC       = 0xC,
        AFTOUCHC = 0xD,
        PITCHB   = 0xE

        # Weirdly enough, doesn't work using enum elements indexes
        # kinda hack
        __names__ = {
            0x8 : "NOTE_OFF" ,
            0x9 : "NOTE_ON " ,
            0xA : "AFTOUCH " ,
            0xB : "CC      " ,
            0xC : "PC      " ,
            0xD : "AFTOUCHC" ,
            0xE : "PITCHB  "
        }

        def __str__( v ):
            return v.__names__.get( int(v), "UKNOWN ")

    ## Class stuff
    def __init__( self, ttype, chan, values ):
        """
        :param ttype: Midi message type (see Type enum)
        :param chan: Midi channel (0-15)
        :param vaules: Midi values (list)

        For a pitch bend message, give only one value in the array with
        a value between 0-16363, for instance values=[8192].
        """
        self.type   = ttype
        self.chan   = chan
        self.values = values

    def __repr__( self ):
        #stype = self.Type.__str__( self.type )
        stype=str(self.type)
        return "{ Midi:%s ; chan=%d, values=%s }" % (
            stype, self.chan, repr(self.values)
        )

    def bytes( self ):
        """
        Get byte representation given a midi message
        :return: a bytes instance with MIDI data
        """
        # status byte encode
        def sbyte( self ): return (int(self.type)<<4)|self.chan

        # encode message with 2 byte arguments
        def c3b( self ):
            return bytes([sbyte(self), self.values[0]&0x7F, self.values[1]&0x7F])

        # encode message with 1 byte argument
        def c2b( self ):
            return bytes([sbyte(self),self.values[0]&0x7F])

        # encode message with 14bit argument (pitchb)
        def c3s( self ):
            return bytes([
                sbyte(self),
                (self.values[0] & 0x007F),
                (self.values[0] & 0x3F80)>>7
            ])

        conv_fkt = {
            self.Type.NOTE_OFF : c3b,
            self.Type.NOTE_ON  : c3b,
            self.Type.AFTOUCH  : c3b,
            self.Type.CC       : c3b,
            self.Type.PC       : c2b,
            self.Type.AFTOUCHC : c2b,
            self.Type.PITCHB   : c3s
        }

        return conv_fkt[self.type](self)

############################################
# Various constructors
############################################
def from_bytes( bb ):
    """
    Construct midi messages from bytes
    :param bb: bytes object to convert midi message from
    :return: Midi_Msg instance
    """
    # status byte => type,chan
    def sbyte(b) : return ( Midi_Msg.Type((b&0xF0)>>4), b&0x0F, )

    # conv 3 byte value
    def c3b(b): return [int(b[1]), int(b[2])]

    # conv 2 btye value
    def c2b(b): return [int(b[1])]

    # conv short (pitchb)
    def c3s(b): return [(int(b[2])<<7) | int(b[1])]

    conv_fkt = {
        Midi_Msg.Type.NOTE_OFF : c3b,
        Midi_Msg.Type.NOTE_ON  : c3b,
        Midi_Msg.Type.AFTOUCH  : c3b,
        Midi_Msg.Type.CC       : c3b,
        Midi_Msg.Type.PC       : c2b,
        Midi_Msg.Type.AFTOUCHC : c2b,
        Midi_Msg.Type.PITCHB   : c3s
    }

    try:
        ttype,chan = sbyte(bb[0])
    except: raise KeyError("Uknown midi message type : %02X" % ((bb[0]&0xF0)>>4) )

    values     = conv_fkt[ttype](bb)

    return Midi_Msg( ttype, chan, values )

def note_off( chan, num, vel ):
    """
    Constructs a note-off message
    :param chan: Midi channel (0-15)
    :param num: Key number
    :param vel: Note velocity
    """

    return Midi_Msg(
        Midi_Msg.Type.NOTE_OFF,
        chan,
        [num,vel]
    )

def note_on( chan, num, vel ):
    """
    Constructs a note-on message
    :param chan: Midi channel (0-15)
    :param num: Key number
    :param vel: Note velocity
    """

    return Midi_Msg(
        Midi_Msg.Type.NOTE_ON,
        chan,
        [num,vel]
    )

def aftouch( chan, num, value ):
    """
    Constructs an Key aftertouch message
    :param chan: Midi channel (0-15)
    :param num: Key number
    :param value: Aftertouch value
    """

    return Midi_Msg(
        Midi_Msg.Type.AFTOUCH,
        chan,
        [num,value]
    )

def cc( chan, num, val ):
    """
    Constructs a Control Change message
    :param chan: Midi channel (0-15)
    :param num: CC number
    :param val: CC val
    :return: Midi_Msg instance
    """

    return Midi_Msg(
        Midi_Msg.Type.CC,
        chan,
        [num,val]
    )

# TODO # Channel mode messages

def pc( chan, num ):
    """
    Program change
    :param chan: Midi channel (0-15)
    :param chan: 
    :return: Midi_Msg instance
    """
    return Midi_Msg(
        Midi_Msg.Type.PC,
        chan,
        [num]
    )

def aftouchc( chan, val ):
    """
    After touch (channel mode)
    :param chan: Midi channel (0-15)
    :param chan: Midi channel (0-15)
    :return: Midi_Msg instance
    """

    return Midi_Msg(
        Midi_Msg.Type.AFTOUCHC,
        chan,
        [val]
    )

def pitchb( chan, val ):
    """
    Constructs pitchb message
    :param chan: Midi channel (0-15)
    :param val: pitchbend position -1 .. 1 => Mapped to 0 .. 16383 range
    :return: Midi_Msg instance
    """

    return Midi_Msg(
        Midi_Msg.Type.PITCHB,
        chan,
        [int(val*8191. + 8192. + .5)]
    )

from MCP3008class import MCP3008class

adc = MCP3008class()
print( adc.read( channel = 0 ) ) # if necessary perform several times

import fileinput

print (" Starting the Formatting of the Json Events..........")

textToSearch = '\\n'
textToReplace = ''
fileToRead = '<path-to-file-read-from>'
fileToWrite = '<path-to-file-write-to>'

readFile = open(fileToRead, 'r')
writeFile = open(fileToWrite, 'w')
formattedEvents = 0
notFormattedEvents = 0
events = 0

for line in fileinput.input(fileToRead):
    events += 1
    if textToSearch in line:
        formattedEvents += 1
        line = line.replace(textToSearch, textToReplace)
    else:
        notFormattedEvents += 1
    # line = ''.join(line.split())
    writeFile.write(line)

readFile.close()
writeFile.close()
print('No Of events', events)
print('Formatted Event count', formattedEvents)
print('Not Formatted Event count', notFormattedEvents)

if events == (formattedEvents + notFormattedEvents):
    print('Formatting went fine')
else:
    print('Check for anomalies in formatting')
print ('End of script')

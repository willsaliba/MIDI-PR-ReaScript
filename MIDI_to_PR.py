RPR_ClearConsole()

#checking if file selected
numSelected = RPR_CountSelectedMediaItems(0)
isMIDI = False
if numSelected == 1:
  
  #if selected extract info from segment
  selectedItem = RPR_GetSelectedMediaItem(0, 0)
  take = RPR_GetTake(selectedItem, 0)
  isMIDI = RPR_TakeIsMIDI(take)
  
  
#output if MIDI
RPR_ShowConsoleMsg("MIDI FILE SELECTED: ")
if isMIDI:
  RPR_ShowConsoleMsg("TRUE")
else: 
  RPR_ShowConsoleMsg("FALSE")


#save MIDI file to "/Users/willsaliba/Downloads"

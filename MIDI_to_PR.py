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
  RPR_ShowConsoleMsg("TRUE\n")
  
  #set location to save MIDI
  save_path = "/Users/willsaliba/Downloads/hooray.midi"
  
  #save MIDI file to selected location ??
  PCM_src = RPR_GetMediaItemTake_Source( take )
  #res = RPR_CF_ExportMediaSource( PCM, save_path )
  
  
else: 
  RPR_ShowConsoleMsg("FALSE\n")
 


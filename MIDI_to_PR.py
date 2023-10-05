from sws_python import CF_ExportMediaSource
RPR_ClearConsole()

#checking if file selected
numSelected = RPR_CountSelectedMediaItems(0)
isMIDI = False

#if selected extract info from segment
if numSelected == 1:
  selectedItem = RPR_GetSelectedMediaItem(0, 0)
  take = RPR_GetTake(selectedItem, 0)
  isMIDI = RPR_TakeIsMIDI(take)
  
#If MIDI try to save segment
RPR_ShowConsoleMsg("MIDI FILE SELECTED: ")
if isMIDI:
  RPR_ShowConsoleMsg("TRUE\n")
  
  #set location to save MIDI
  save_path = "/Users/willsaliba/Downloads/topics/reaper/M_to_PR/hooray.midi"

  #saving MIDI segment using SWS function (with take & pcm_src)
  PCM_src = RPR_GetMediaItemTake_Source(take)
  save_succeded = CF_ExportMediaSource(PCM_src, save_path) 
  
else: 
  RPR_ShowConsoleMsg("FALSE\n")
  
#if save succeeded convert to piano roll
if save_succeded:

  RPR_ShowConsoleMsg("\n\nFILE SAVED TO: " + save_path)
  
  RPR_ShowConsoleMsg("\n\nConverting to Piano Roll...")
  #!!! insert jacks code here
  
  
else:
  RPR_ShowConsoleMsg("\n\nFILE FAILED TO SAVE")
 



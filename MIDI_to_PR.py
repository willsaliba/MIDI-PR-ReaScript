from sws_python import CF_ExportMediaSource
RPR_ClearConsole()

isMIDI = False
save_succeded = False

#checking if file selected
numSelected = RPR_CountSelectedMediaItems(0)

#if selected extract info from segment
if numSelected == 1:
  selectedItem = RPR_GetSelectedMediaItem(0, 0)
  take = RPR_GetTake(selectedItem, 0)
  isMIDI = RPR_TakeIsMIDI(take)
  
#If MIDI try to save segment
if isMIDI:
  RPR_ShowConsoleMsg("MIDI FILE SELECTED\n")
  
  #set location to save MIDI
  save_dir = "/Users/willsaliba/Documents/Topics/ReaScripts/outputs"
  midi_path = save_dir + "/original.mid"
  

  #saving MIDI segment using SWS function (with take & pcm_src)
  PCM_src = RPR_GetMediaItemTake_Source(take)
  save_succeded = CF_ExportMediaSource(PCM_src, midi_path)
  
else: 
  RPR_ShowConsoleMsg("MIDI FILE NOT SELECTED\n")
  
#if save succeeded convert to piano roll
if save_succeded:

  RPR_ShowConsoleMsg("\n\nFILE SAVED TO: " + midi_path)
  RPR_ShowConsoleMsg("\n\nConverting to Piano Roll...")
  
  #INSERT SCRIPT.PY HERE
  
  
  
  #RPR_ShowConsoleMsg("\n\nINSTRUMENT ROLLS SAVED")
  
else:
  RPR_ShowConsoleMsg("\n\nNO ACTION TAKEN")
 



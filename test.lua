reaper.ClearConsole()

-- Check if a file is selected
numSelected = reaper.CountSelectedMediaItems(0)
isMIDI = false

-- If a file is selected, extract info from segment
if numSelected == 1 then
  selectedItem = reaper.GetSelectedMediaItem(0, 0)
  take = reaper.GetTake(selectedItem, 0)
  isMIDI = reaper.TakeIsMIDI(take)
end

-- Output if MIDI
reaper.ShowConsoleMsg("MIDI FILE SELECTED: ")
if isMIDI then
  reaper.ShowConsoleMsg("TRUE")
  
  -- Set location to save MIDI
  save_path = "/Users/willsaliba/Downloads/topics/reaper/M_to_PR/hooray.midi"
  
  --///////pythonified till here/////////
    
  --saving MIDI segment using take & pcm_src then output result
  PCM_src = reaper.GetMediaItemTake_Source(take)
  res = reaper.CF_ExportMediaSource(PCM_src, save_path)
  if res then 
    reaper.ShowConsoleMsg("\n\nFILE SAVED TO: " .. save_path)
  else 
    reaper.ShowConsoleMsg("\n\nFILE FAILED TO SAVE")
  end
  
else 
  reaper.ShowConsoleMsg("FALSE\n")
end

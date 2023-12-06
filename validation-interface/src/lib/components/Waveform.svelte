<script>
    // Import dependencies:
    import { onMount } from 'svelte';
    import WaveSurfer from 'wavesurfer.js';
    import RegionsPlugin from '$lib/scripts/regions_plug.js';
    import ZoomPlugin from '$lib/scripts/zoom_plug.js';
    import { createEventDispatcher } from 'svelte'

    const dispatch = createEventDispatcher();

    // Local variables:
    let wavesurfer;
    let wsRegions;
    let selected_region;
    let selected_col = "rgba(0,0,255,0.5)";
    let word_col = "rgba(255,0,0,0.5)";
    let silence_col = "rgba(0,255,0,0.5)";

    onMount(async () => {
		wavesurfer = WaveSurfer.create({
            container: '#waveform',
            waveColor: '#4F4A85',
            progressColor: '#383351',
            mediaControls: true,
            minPxPerSec: 100
        });

        wavesurfer.on('decode', () =>{
            dispatch("audio_loaded");
        });

        wsRegions = wavesurfer.registerPlugin(RegionsPlugin.create());
        wavesurfer.registerPlugin(ZoomPlugin.create({scale: 0.2,}));
	});

    export const update_audio_src = async (path) => {
        wavesurfer.load(path);
    };

    export const select_resion_from_index = (index) => {
        select_region(wsRegions.regions[index]);
    };

    export const update_regions = (slice_data) => {
        wsRegions.clearRegions();

        for(let i = 0; i < slice_data["slices"].length; i++){
            let col = word_col;
            if(slice_data["slices"][i]["type"] === "silence"){
                col = silence_col;
            };
            if(slice_data["slices"][i]["selected"]){
                col = selected_col;
            };

            wsRegions.addRegion({
                start : slice_data["slices"][i]["start"],
                end : slice_data["slices"][i]["end"],
                content: String(i),
                color: col,
                drag: false,
                resize: true,
                id : "region_" + String(i) + "_" + slice_data["slices"][i]["type"]
            });
        };

        wsRegions.on('region-updated', (region) => {
            //console.log('Updated region', region);
            slice_data["slices"][region.id.split("_")[1]]["start"] = region.start;
            slice_data["slices"][region.id.split("_")[1]]["end"] = region.end;
            dispatch("change_value")
        });
        
        wsRegions.on('region-clicked', (region, e) => {
            e.stopPropagation(); // prevent triggering a click on the waveform
            select_region(region);
            dispatch("selected_slice", {index : region.id.split("_")[1]});
        });

        wsRegions.on('region-out', (region) => {
            if (selected_region === region) {
                wavesurfer.pause();
            };
        });
    };

    function select_region(region){
        selected_region = region;
        region.play(region.start, region.end);

        for(let reg of wsRegions.regions){
            let this_type = reg.id.split("_")[2];
            if(this_type === "word"){
                reg.setOptions({ color: word_col })
            }else{
                reg.setOptions({ color: silence_col })
            }
        }
        region.setOptions({ color: selected_col });
    }
</script>

<div>
    <div id="waveform"></div>
</div>
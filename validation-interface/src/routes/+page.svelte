<script>
    // Import dependencies
    import { onMount } from 'svelte';
    import * as server_utils from "$lib/scripts/server_utils.js";
    import * as utils from "$lib/scripts/utils.js";

    // Import components
    import Waveform from '$lib/components/Waveform.svelte';
    import SliceTable from '$lib/components/SliceTable.svelte';
    
    // Local variables:
    let waveform_bind;
    let slice_table_bind;
    let open_data;
    let slice_data = {"slices" : []};

    onMount(async () => {
        // Get most recent open data:
        await get_most_recent_open_data();

        // Initialize audio and slice data:
        await waveform_bind.update_audio_src("sessions/" + open_data["uuid"] + "/audio.wav");
        slice_data = await server_utils.read_json("static/sessions/" + open_data["uuid"] + "/slice_data.json");
        for(let slice of slice_data["slices"]){
            slice["selected"] = false;
        };
	});

    function handle_audio_loaded(){
        waveform_bind.update_regions(slice_data);
    };

    async function get_most_recent_open_data(){
        let open_file_list = await server_utils.getFiles("src/lib/data/open_files");
        if(open_file_list.length > 0){
            let sorted = open_file_list.sort(function(a,b) {
                return utils.date_string_to_float(b.creation) - utils.date_string_to_float(a.creation);
            });
            open_data = await server_utils.read_json(sorted[0]["path"]);
        };
    };

    function handle_select_slice(e){
        waveform_bind.select_resion_from_index(e.detail.index);
    };

    function handle_waveform_selected_slice(e){
        for(let slice of slice_data["slices"]){
            slice["selected"] = false;
        };
        slice_data["slices"][e.detail.index]["selected"] = true;
        slice_table_bind.scroll_to_slice(e.detail.index);
    }

    function handle_slice_table_change_value(){
        waveform_bind.update_regions(slice_data);
    };

    function handle_waveform_change_value(){
        slice_data = slice_data;
    }
</script>

<Waveform
    bind:this = {waveform_bind}
    on:audio_loaded = {() => handle_audio_loaded()}
    on:selected_slice = {(e) => handle_waveform_selected_slice(e)}
    on:change_value = {() => handle_waveform_change_value()}
/>

<SliceTable
    bind:this = {slice_table_bind}
    bind:slice_data = {slice_data}
    on:select_slice = {(e) => handle_select_slice(e)}
    on:change_value = {() => handle_slice_table_change_value()}
/>
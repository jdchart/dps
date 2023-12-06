<script>
    import { createEventDispatcher } from 'svelte'

    const dispatch = createEventDispatcher()
    export let slice_data;

    function handle_click(event, index){
        //console.log(slice_data["slices"][index]);
        for(let slice of slice_data["slices"]){
            slice["selected"] = false;
        };
        slice_data["slices"][index]["selected"] = true;
        dispatch("select_slice", {index : index})
    };

    function get_row_class(row_type){
        if(row_type === "word"){
            return "word_row";
        }
        else{
            return "silence_row";
        };
    };

    function handle_value_change(){
        dispatch("change_value")
    }

    export const scroll_to_slice = (index) => {
        document.getElementById("slice_" + String(index)).scrollIntoView();
    }

    function handle_add_slice_button(e){
        e.stopPropagation();
        console.log("hello world")
    }
</script>

<div class="slice_list_container">
    <div class="table_head grid_area">
        <p>Idx</p>
        <p>Start</p>
        <p>End</p>
        <p>Duration</p>
        <p>Type</p>
        <p>Props</p>
    </div>

    <div class="scrollable_area">
        {#each slice_data["slices"] as slice, i}
            <div class="table_row grid_area {get_row_class(slice.type)} {slice.selected ? 'selected_slice' : ''}" id="slice_{String(i)}">
                <div on:click={(e) => handle_click(e, i)} class="index_container">
                    <p><span style="font-weight: bold;">{i}</span></p>
                    <button on:click={(e) => handle_add_slice_button(e)}>+&#8593;</button>
                    <button on:click={(e) => handle_add_slice_button(e)}>+&#8595;</button>
                    <button on:click={(e) => handle_add_slice_button(e)}>-</button>
                </div>
                <div class="input_container">
                    <input type="number" step="0.001" bind:value={slice.start} on:change={() => handle_value_change()}>
                </div>
                <div class="input_container">
                    <input type="number" step="0.001" bind:value={slice.end}>
                </div>
                <p>{slice.duration.toFixed(3)}</p>
                <p>{slice.type}</p>
                <div class="prop_container">
                    {#each Object.keys(slice.props) as prop_key}
                        <p><span style="font-weight: bold;">{prop_key}</span> : {slice.props[prop_key]} </p>
                    {/each}
                </div>
            </div>
        {/each}
    </div>
</div>

<style>
    input{
        width: 100%;
    }

    .index_container{
        display: flex;
        flex-wrap: wrap;
        align-items: center;
        gap: 0.3em;
    }

    .index_container:hover{
        cursor: pointer;
    }

    .input_container{
        width: 100%;
        padding: 0.2em;
    }

    p{
        padding: 0.2em;
    }

    .slice_list_container{
        height: 400;
        width: 80%;
        margin: 0.5em;
        border: 1px solid grey;
    }

    .table_head{
        border-bottom: 1px solid grey;
        height: 50px;
        font-weight: bold;
    }

    .grid_area{
        display: grid;
        grid-template-columns: 1fr 1fr 1fr 1fr 1fr 3fr;
        grid-gap: 0.4em;
        width: 100%;
        align-items: center;
    }

    .scrollable_area{
        overflow-y: scroll;
        height: 350px;
    }

    .table_row{
        padding: 0.2em;
    }

    .table_row:hover{
        border: 1px solid grey;
    }

    .prop_container{
        display: flex;
        gap: 0.3em;
    }

    .word_row{
        background-color: rgba(255,0,0,0.5);
    }

    .silence_row{
        background-color: rgba(0,255,0,0.5);
    }

    .selected_slice{
        background-color: rgba(0,0,255,0.5);
    }
</style>
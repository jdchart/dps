<script>
    import { onMount } from 'svelte';
    import WaveSurfer from 'wavesurfer.js';

    export let audio_file;

    onMount(async () => {
		const wavesurfer = WaveSurfer.create({
            container: '#waveform',
            waveColor: '#4F4A85',
            progressColor: '#383351',
            url: audio_file,
            mediaControls: true,
        })

        wavesurfer.on('click', () => {
            wavesurfer.play();
        })
	});
</script>

<div>
    <h2>Waveform</h2>
    <div id="waveform"></div>
</div>
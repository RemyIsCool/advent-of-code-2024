<script lang="ts">
	import { fade, slide } from 'svelte/transition';

	let stones = $state([125, 17]);
	let done = $state(false);

	const iterations = 5;

	$effect(() => {
		let count = 0;

		const interval = setInterval(() => {
			if (count >= iterations - 1) {
				clearInterval(interval);
				setTimeout(() => (done = true), 3000);
			}

			const nextStones: number[] = [];

			for (const stone of stones) {
				if (stone === 0) {
					nextStones.push(1);
				} else if (stone.toString().length % 2 === 0) {
					nextStones.push(
						parseInt(stone.toString().slice(0, stone.toString().length / 2)),
						parseInt(stone.toString().slice(stone.toString().length / 2))
					);
				} else {
					nextStones.push(stone * 2024);
				}
			}

			stones = nextStones;

			count++;
		}, 3000);

		() => clearInterval(interval);
	});
</script>

<div class="grid min-h-screen px-8 py-10">
	{#if done}
		<p
			transition:fade
			class="col-span-full row-span-full mb-12 grid place-content-center text-center text-5xl"
		>
			The amount of stones after {iterations} blinks is: <strong>{stones.length}</strong>
		</p>
	{:else}
		<div transition:fade class="col-span-full row-span-full grid place-content-center pb-48">
			<h1 class="mx-auto mb-12 w-3/4 text-center text-5xl font-bold">
				Advent of Code - Day 11: Plutonian Pebbles
			</h1>
			<div class="flex flex-wrap justify-center gap-6">
				{#each stones as stone}
					<p
						in:slide={{ axis: 'x' }}
						class="rounded-xl border-2 border-slate-600 px-10 py-6 text-4xl"
					>
						{stone}
					</p>
				{/each}
			</div>
		</div>
	{/if}
</div>

<style>
	:global(body) {
		@apply bg-slate-900 text-slate-100;
	}
</style>

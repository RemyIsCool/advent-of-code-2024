<script lang="ts">
	import { flip } from 'svelte/animate';
	import { slide } from 'svelte/transition';

	type Stone = {
		value: number;
		id: number;
	};

	let stones = $state<Stone[]>([125, 17].map((num) => ({ value: num, id: Math.random() })));

	$effect(() => {
		let count = 0;

		const interval = setInterval(() => {
			if (count >= 25) {
				clearInterval(interval);
			}

			const nextStones: Stone[] = [];

			for (const stoneObj of stones) {
				const stone = stoneObj.value;

				if (stone === 0) {
					nextStones.push({ ...stoneObj, value: 1 });
				} else if (stone.toString().length % 2 === 0) {
					nextStones.push(
						{
							value: parseInt(stone.toString().slice(0, stone.toString().length / 2)),
							id: Math.random()
						},
						{
							value: parseInt(stone.toString().slice(stone.toString().length / 2)),
							id: Math.random()
						}
					);
				} else {
					nextStones.push({ ...stoneObj, value: stone * 2024 });
				}
			}

			stones = nextStones;

			count++;
		}, 3000);

		() => clearInterval(interval);
	});
</script>

<div class="grid">
	<div class="col-span-full row-span-full grid min-h-screen place-content-center pb-48">
		<h1 class="mx-auto mb-12 w-3/4 text-center text-5xl font-bold">
			Advent of Code - Day 11: Plutonian Pebbles
		</h1>
		<div class="flex flex-wrap justify-center gap-6">
			{#each stones as stone (stone.id)}
				<p
					animate:flip
					in:slide={{ axis: 'x' }}
					class="rounded-xl border-2 border-slate-600 px-10 py-6 text-4xl"
				>
					{stone.value}
				</p>
			{/each}
		</div>
	</div>
</div>

<style>
	:global(body) {
		@apply bg-slate-900 text-slate-100;
	}
</style>

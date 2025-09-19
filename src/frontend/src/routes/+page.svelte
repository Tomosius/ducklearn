<!-- src/frontend/src/routes/+page.svelte -->
<script lang="ts">
	import { onMount } from 'svelte';

	let name = 'DuckLearn';
	let result = '';
	let ready = false;

	function callHello() {
		const api = (window as any)?.pywebview?.api;
		if (api?.hello) {
			api.hello(name).then((res: string) => (result = res));
		}
	}

	onMount(() => {
		const w = window as any;
		if (w.pywebview) {
			ready = true;
		} else {
			window.addEventListener('pywebviewready', () => (ready = true), { once: true });
		}
	});
</script>

<main class="min-h-screen text-slate-900 dark:text-slate-100">
	<div class="mx-auto max-w-xl px-6 py-12">
		<div class="mb-6 flex items-center gap-3">
			<div class="flex h-10 w-10 items-center justify-center rounded-xl bg-indigo-600/10">
				<span class="font-black text-indigo-600">DL</span>
			</div>
			<h1 class="text-2xl font-semibold tracking-tight">DuckLearn</h1>

			<span
				class={'ml-auto inline-flex items-center gap-2 rounded-full px-3 py-1 text-xs font-medium ' +
					(ready ? 'bg-green-100 text-green-800' : 'bg-amber-100 text-amber-800')}
			>
				<span class={'size-2 rounded-full ' + (ready ? 'bg-green-500' : 'bg-amber-500')} />
				{ready ? 'bridge ready' : 'waiting for bridge'}
			</span>
		</div>

		<div
			class="rounded-2xl border border-slate-200/70 bg-white/70 p-6 shadow-sm backdrop-blur
                dark:border-slate-800 dark:bg-slate-900/60"
		>
			<label for="name" class="mb-2 block text-sm font-medium text-slate-600 dark:text-slate-300">
				Your name
			</label>

			<div class="flex items-stretch gap-2">
				<input
					id="name"
					bind:value={name}
					placeholder="Your name"
					class="w-full rounded-xl border border-slate-300 bg-white px-3 py-2 ring-2
                 ring-transparent transition outline-none focus:border-indigo-500 focus:ring-indigo-200
                 dark:border-slate-700 dark:bg-slate-800 dark:focus:ring-indigo-900/40"
				/>

				<button
					on:click={callHello}
					disabled={!ready}
					class="rounded-xl bg-indigo-600 px-4 py-2 font-medium text-white transition
                 hover:bg-indigo-500 disabled:cursor-not-allowed disabled:opacity-40"
				>
					Say hello
				</button>
			</div>

			{#if result}
				<p class="mt-4 text-sm text-slate-700 dark:text-slate-200">
					<span class="mr-2">Response:</span>
					<span class="inline-block rounded-lg bg-slate-100 px-2 py-1 font-mono dark:bg-slate-800">
						{result}
					</span>
				</p>
			{/if}
		</div>

		<p class="mt-8 text-xs text-slate-500">
			Tailwind test: you should see a gradient background, rounded inputs, focus rings, and colored
			status pill.
		</p>
	</div>
</main>

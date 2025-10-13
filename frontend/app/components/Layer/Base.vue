<script lang="ts" setup>
    const rootSettingsStore = useRootSettingsStore()
    const domainStore = useDomainStore()
    await domainStore.setDomains()

    onMounted(() => {
        if (!rootSettingsStore.settings?.scripts) return
        const container = document.createElement('div')
        container.innerHTML = rootSettingsStore.settings.scripts
        container.querySelectorAll('script').forEach(script => {
            const createdScript = document.createElement('script')
            createdScript.textContent = script.innerHTML
            document.body.insertAdjacentElement('beforebegin', createdScript)
        })
    })
</script>

<template>
    <div class="wrapper">
        <Header />
        <main class="main">
            <slot></slot>
        </main>
        <Footer />
        <WidgetCookieBanner />
        <ModalCallback />
    </div>
</template>

<style lang="scss" scoped>
    .wrapper {
        width: 100%;
        min-height: 100vh;
        overflow: clip;
        display: flex;
        flex-direction: column;
    }

    .main {
        flex: 0 1 auto;
    }
</style>
